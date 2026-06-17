"""Storage manager for configuration and state persistence."""

import json
import os
import re
import shutil
from pathlib import Path
from typing import Any, List

from pydantic import ValidationError

from ..models import Config


# Matches ${VAR_NAME} in string config values. Names follow env-var rules
# (ASCII letters, digits, underscore; must not start with a digit).
_ENV_VAR_PATTERN = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")


def _expand_env_vars(value: Any) -> Any:
    """Recursively expand ``${VAR}`` references inside any string leaves.

    Containers (dicts, lists, tuples) are walked; non-string leaves are
    returned unchanged. Strings with no ``${...}`` tokens are returned
    unchanged. References to unset variables are **left as-is**, so
    ``${MISSING}`` round-trips to ``${MISSING}`` and surfaces as a clear
    downstream error rather than a silent empty string.

    This is intentionally identical to the behaviour ``RSSScraper`` uses
    for RSS feed URLs, so a single ``${VAR}`` convention works everywhere
    in the config (AI ``base_url``, feed URLs, webhook URLs, ...).
    """
    if isinstance(value, str):
        return _ENV_VAR_PATTERN.sub(
            lambda m: os.environ.get(m.group(1), m.group(0)),
            value,
        )
    if isinstance(value, dict):
        return {k: _expand_env_vars(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_expand_env_vars(v) for v in value]
    if isinstance(value, tuple):
        return tuple(_expand_env_vars(v) for v in value)
    return value


class ConfigError(ValueError):
    """Raised when configuration is missing or invalid."""

    pass


class StorageManager:
    """Manages file-based storage for configuration and state."""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.config_path = self.data_dir / "config.json"
        self.summaries_dir = self.data_dir / "summaries"

        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.summaries_dir.mkdir(parents=True, exist_ok=True)

    def load_config(self) -> Config:
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {self.config_path}\n"
                f"Please create it based on the template in README.md"
            )

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise ConfigError(
                f"Invalid JSON in configuration file: {self.config_path}\n" f"Error: {e}"
            ) from e

        # Expand ${VAR} references in every string value before pydantic
        # validation. Keeps credentials / private endpoints / tenant IDs
        # out of the JSON file so it is safe to commit to a public repo.
        data = _expand_env_vars(data)

        try:
            return Config.model_validate(data)
        except ValidationError as e:
            raise ConfigError(
                f"Configuration validation failed for {self.config_path}\n"
                f"Details: {e}"
            ) from e

    def save_config(self, config: Config, backup: bool = True) -> Path:
        """Save configuration to config.json, optionally backing up the existing file.

        Args:
            config: The Config object to save.
            backup: If True and config.json exists, copy it to config.json.bak first.

        Returns:
            Path to the saved config file.
        """
        if backup and self.config_path.exists():
            shutil.copy2(self.config_path, self.config_path.with_suffix(".json.bak"))

        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(config.model_dump(mode="json"), f, indent=2, ensure_ascii=False)
            f.write("\n")

        return self.config_path

    def save_daily_summary(self, date: str, markdown: str, language: str = "en") -> Path:
        """Save daily summary to data/summaries/ with Jekyll front matter.

        The summary markdown is wrapped with a YAML front matter block so
        that downstream tooling (e.g. the GitHub Pages deploy step that
        copies these files into docs/_posts/) gets a valid Jekyll post
        out of the box. Without front matter Jekyll treats the file as a
        static page, so site.posts filters (e.g. ``where: "lang", "zh"``)
        in index.md silently drop them and the digest list shows
        "No posts yet".

        The filename MUST start with ``YYYY-MM-DD-`` because GitHub Pages
        ships Jekyll 3, which only recognises a file as a post when the
        basename begins with a date. A leading ``horizon-`` prefix
        (e.g. ``horizon-2026-06-17-zh.md``) gets silently skipped and
        site.posts ends up empty even when front matter is correct.

        Front matter includes ``period: daily`` so the home page can
        group the four roll-up types into separate sections.
        """
        filename = f"{date}-horizon-{language}.md"
        return self._write_period_post(
            filename=filename,
            markdown=markdown,
            period="daily",
            period_id=date,
            language=language,
        )

    def save_weekly_summary(
        self, iso_week_id: str, markdown: str, language: str = "en"
    ) -> Path:
        """Save a weekly roll-up summary.

        Args:
            iso_week_id: ISO 8601 week identifier, e.g. ``2026-W25``.
            markdown: Generated weekly report body.
            language: ``en`` or ``zh``.

        Returns:
            Path to the saved file under data/summaries/.
        """
        filename = f"{iso_week_id}-horizon-{language}.md"
        return self._write_period_post(
            filename=filename,
            markdown=markdown,
            period="weekly",
            period_id=iso_week_id,
            language=language,
        )

    def save_monthly_summary(
        self, year_month: str, markdown: str, language: str = "en"
    ) -> Path:
        """Save a monthly roll-up summary.

        Args:
            year_month: ``YYYY-MM`` identifier, e.g. ``2026-06``.
        """
        filename = f"{year_month}-horizon-{language}.md"
        return self._write_period_post(
            filename=filename,
            markdown=markdown,
            period="monthly",
            period_id=year_month,
            language=language,
        )

    def save_yearly_summary(
        self, year: str, markdown: str, language: str = "en"
    ) -> Path:
        """Save a yearly roll-up summary.

        Args:
            year: ``YYYY`` identifier, e.g. ``2026``.
        """
        filename = f"{year}-horizon-{language}.md"
        return self._write_period_post(
            filename=filename,
            markdown=markdown,
            period="yearly",
            period_id=year,
            language=language,
        )

    def list_recent_summaries(
        self,
        period: str,
        language: str = "zh",
        since_id: str = "",
        until_id: str = "",
    ) -> List[Path]:
        """List existing summary files for a given period + language.

        ``period`` is one of ``daily``, ``weekly``, ``monthly``, ``yearly``.
        The id format depends on the period:
        - daily: ``YYYY-MM-DD``
        - weekly: ``YYYY-Www`` (ISO week, e.g. ``2026-W25``)
        - monthly: ``YYYY-MM``
        - yearly: ``YYYY``

        ``since_id`` and ``until_id`` are inclusive string bounds used
        for lexical comparison.
        """
        if period not in {"daily", "weekly", "monthly", "yearly"}:
            raise ValueError(f"unknown period: {period}")
        suffix = f"-horizon-{language}.md"
        results: List[Path] = []
        for path in self.summaries_dir.iterdir():
            if not path.name.endswith(suffix):
                continue
            prefix = path.name[: -len(suffix)]
            if not self._period_id_matches(prefix, period):
                continue
            period_id = prefix
            if since_id and period_id < since_id:
                continue
            if until_id and period_id > until_id:
                continue
            results.append(path)
        results.sort()
        return results

    @staticmethod
    def _period_id_matches(prefix: str, period: str) -> bool:
        """Return True if a summary filename prefix looks like a period id."""
        if period == "daily":
            parts = prefix.split("-")
            return len(parts) == 3 and all(p.isdigit() for p in parts)
        if period == "weekly":
            return (
                len(prefix) == 8
                and prefix[:4].isdigit()
                and prefix[4] == "-"
                and prefix[5] == "W"
                and prefix[6:].isdigit()
            )
        if period == "monthly":
            parts = prefix.split("-")
            return len(parts) == 2 and all(p.isdigit() for p in parts)
        if period == "yearly":
            return prefix.isdigit() and len(prefix) == 4
        return False

    def _write_period_post(
        self,
        filename: str,
        markdown: str,
        period: str,
        period_id: str,
        language: str,
    ) -> Path:
        """Shared writer for daily / weekly / monthly / yearly posts.

        All four pass through the same front-matter + H1 strip logic so
        downstream tooling (the Pages deploy step, the home-page Jekyll
        template, and ``list_recent_summaries``) sees a consistent shape.
        """
        filepath = self.summaries_dir / filename

        content = markdown
        first_line = content.strip().split("\n", 1)[0]
        if first_line.startswith("# "):
            parts = content.split("\n", 1)
            if len(parts) > 1:
                content = parts[1].lstrip("\n")

        period_titles = {
            "daily": "Horizon Daily",
            "weekly": "Horizon Weekly",
            "monthly": "Horizon Monthly",
            "yearly": "Horizon Yearly",
        }
        title = f"{period_titles[period]}: {period_id} ({language.upper()})"

        front_matter = (
            "---\n"
            "layout: default\n"
            f'title: "{title}"\n'
            f"date: {period_id}\n"
            f"lang: {language}\n"
            f"period: {period}\n"
            f"period_id: {period_id}\n"
            "---\n\n"
        )

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(front_matter + content)

        return filepath

    def load_subscribers(self) -> list:
        """Loads the list of email subscribers."""
        subscribers_path = self.data_dir / "subscribers.json"
        if not subscribers_path.exists():
            return []

        try:
            with open(subscribers_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def add_subscriber(self, email_addr: str):
        """Adds a new subscriber email."""
        subscribers = self.load_subscribers()
        if email_addr not in subscribers:
            subscribers.append(email_addr)
            self._save_subscribers(subscribers)

    def remove_subscriber(self, email_addr: str):
        """Removes a subscriber email."""
        subscribers = self.load_subscribers()
        if email_addr in subscribers:
            subscribers.remove(email_addr)
            self._save_subscribers(subscribers)

    def _save_subscribers(self, subscribers: list):
        """Helper to save subscribers list."""
        subscribers_path = self.data_dir / "subscribers.json"
        with open(subscribers_path, "w", encoding="utf-8") as f:
            json.dump(subscribers, f, indent=2)
