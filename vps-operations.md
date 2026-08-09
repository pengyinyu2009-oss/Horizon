# Horizon VPS operations

The production daily pipeline is owned by the VPS. GitHub Actions schedules are
disabled so there is only one scheduler.

## Schedule

The production crontab runs `run-daily.sh` in local mode at 08:17 Beijing time.
The 10:30 and 21:17 entries are idempotent completion retries. A retry exits
immediately when the dated report and public lineage are current. If generation
finished but site publication failed, it republishes the verified artifacts
without calling the AI models again.

```cron
17 8 * * * HORIZON_EXECUTION_MODE=local /home/pengyinyu/Horizon/run-daily.sh
30 10 * * * HORIZON_EXECUTION_MODE=local /home/pengyinyu/Horizon/run-daily.sh
17 21 * * * HORIZON_EXECUTION_MODE=local /home/pengyinyu/Horizon/run-daily.sh
```

`run-daily.sh` defaults to local mode. `scripts/dispatch_daily_github.py` is an
explicit manual recovery path and is not scheduled. It requires a GitHub token
that is allowed to dispatch Actions workflows:

```bash
HORIZON_EXECUTION_MODE=github ./run-daily.sh
```

## Publication recovery

Generation and publication are separate durable states in
`output/last-success.json`. A complete generated set is recorded with
`published=false` before rendering begins. A later run validates the five
artifacts and lineage, then resumes publication only. Set `HORIZON_FORCE=1`
when intentional regeneration is required.

Each board configuration is mounted read-only at `/app/data/config.json` for
its container run. The host `data/config.json` is never swapped, so an abrupt
process kill cannot leave the next run on the wrong board configuration.

## Log rotation

`run-daily.sh` trims the active log to its most recent 1 MiB before appending.
This user-level safety limit is active without root access. Override it with
`HORIZON_RUN_LOG_MAX_BYTES` when needed.

For compressed historical generations, install the optional checked-in policy
once on a host that has `logrotate`, then validate it without forcing a rotation:

```bash
sudo install -m 0644 deploy/horizon-logrotate.conf /etc/logrotate.d/horizon
sudo logrotate --debug /etc/logrotate.d/horizon
```

The optional policy rotates daily or at 1 MiB, retains 14 compressed
generations, and uses `copytruncate` so the shell redirection can remain open
safely.
