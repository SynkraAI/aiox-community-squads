# SOP: Daily Backup Verification

## Purpose
Verify daily backups completed successfully and are restorable.

## Procedure
1. Open backup dashboard and filter by current date.
2. Confirm all scheduled jobs have status `SUCCESS`.
3. Restore one random backup to staging and run checksum.
4. Record verification result in the ops log.
5. Escalate to `sop-auditor` if any verification step fails.
