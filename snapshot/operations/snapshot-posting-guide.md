---
title: "Snapshot Flat File — Posting Requests"
id: snapshot-flatfile-posting-guide
categories: SIS, Snapshot Flat File
published: "2026-07-10"
edited: "2026-07-10"
author: "Jeff Kelley, Principal Solutions Engineer, Blackboard Inc."
---

# Posting Requests

## In Plain Terms

Think of a Snapshot Flat File like mailing a package to Blackboard Learn. You pack your data — a list of users, courses, enrollments, whatever you're sending — into a plain text file, formatted a specific way. You send that file over the internet to a specific web address at your Learn instance. Learn opens the package, processes what's inside, and hands you back a tracking number so you can check whether everything inside arrived and was accepted.

This guide covers that shipping process, step by step: how to address and send the package (the HTTP request), how to read the receipt you get back, and how to use the tracking number to confirm it was actually processed — not just delivered.

---

Operational guidance for constructing and executing the HTTP requests that submit Snapshot Flat File data to Blackboard Learn. This complements the field-level object specs — start there for file format and required fields per object; use this doc when you're ready to actually send a request.

> As with the rest of this repository, this content is provided as-is, without warranty or support of any kind — Blackboard retains all rights. Always confirm current behavior against your own Learn instance and Blackboard's official documentation before relying on it.

---

## Request Template

Every Snapshot Flat File request is an HTTPS POST with HTTP Basic Auth and the file as the raw request body.

```text
POST https://{learn-host}/webapps/bb-data-integration-flatfile-{deployment-id}/endpoint/{object}/{operation}
Authorization: Basic base64(username:password)
Content-Type: text/xml
```

`curl` equivalent, parameterized:

```bash
curl -w "\n%{http_code}\n" \
  -H "Content-Type: text/xml" \
  -u "${SNAPSHOT_USERNAME}:${SNAPSHOT_PASSWORD}" \
  --data-binary @"${FILE_PATH}" \
  "https://${LEARN_HOST}/webapps/bb-data-integration-flatfile-${DEPLOYMENT_ID}/endpoint/${OBJECT}/${OPERATION}"
```

- `{object}` — endpoint slug from the [Overview](../snapshot-flat-file-overview.md#complete-endpoint-reference) table, e.g. `person`, `course`, `membership`.
- `{operation}` — `store`, `refresh`, or `delete`.
- `-k` (insecure/skip TLS verification) should only ever be used against a known test/sandbox host with a self-signed cert — never against production.
- `-w "%{http_code}"` surfaces the HTTP status code so a failed request isn't mistaken for success.

---

## Response Format

A successful POST returns a plain-text acknowledgement containing a reference code — this is the `dataSetUid` used to check processing status:

```text
Success: Feed File Uploaded. Use the reference code afc3d6e84df84f51944a06cccee8f59a to track these records in the logs.
```

Capture this reference code from the response body. A 2xx/success response here means the file was *accepted for processing* — Learn processes data sets asynchronously, so it does not mean every record has been applied yet. Use the `dataSetUid` with the [Checking Processing Status](#checking-processing-status) endpoint below to confirm completion.

---

## Pre-Flight Checklist

Run through this before firing any request that isn't a `store` against a test environment:

1. **Confirm the target host.** Double-check `{learn-host}` resolves to the environment you intend (Test/Stage vs. Production). It's easy to fire a script at the wrong environment.
2. **Confirm the operation.** `store` is additive/idempotent (smart insert-or-update). `refresh` will disable or purge any record *not* present in the submitted file across the whole integration. `delete` acts only on records listed in the file. See the [Delete Behaviors](../snapshot-flat-file-overview.md#delete-behaviors) table — some objects are purged, not disabled, and purge is not recoverable. See [REFRESH Risk](#refresh-risk) below before relying on `refresh` for a recurring feed.
3. **Confirm the Data Source Key.** It must already exist in **Administrator Panel > Data Integration > Data Source Keys**, and must match what the file (or the integration config) expects.
4. **Validate the file before sending.** Header row present, pipe-delimited, UTF-8, required columns per the relevant object spec. Sending a malformed file to `refresh` is more costly than to `store` since it defines "everything that should still exist."
5. **Dry-run on Test/Stage first** for anything other than a small `store` batch, if a non-production Learn instance is available to you.
6. **Check the response code and body**, not just "the command exited." A 2xx response acknowledges receipt — it does not by itself guarantee every record processed without error.
7. **Follow up on processing status.** Learn processes submitted data sets asynchronously; capture the `dataSetUid` from the response and poll the status endpoint below to confirm the batch actually completed and to check for per-record errors, rather than assuming success from the POST response alone.
8. **Budget more time for `refresh` than `store`.** Complete Refresh operations process the full managed set and can take noticeably longer than a `store` of the same file size — this matters when scheduling recurring jobs (see [Automating Requests](#automating-requests)) so a slow refresh doesn't overlap the next scheduled run.
9. **Log what you did** (host, object, operation, filename, timestamp, initiator) somewhere durable for audit purposes — but never log the credentials themselves.

---

## REFRESH Risk

`refresh` operates against an entire managed data set — potentially every user, course, or enrollment an institution has — not just the records that actually changed. That makes it inherently riskier than `store`, in a few concrete ways:

- **Large data sets mean large files and heavy processing.** A refresh against a full population is a much bigger job for Learn to process than an incremental `store`, and simply takes longer to run — see checklist item 8 above.
- **An interrupted or truncated file doesn't just fail — it actively damages data.** If the request is interrupted mid-transfer, or the file gets truncated before Learn receives all of it, Learn still treats what it *did* receive as "this is everything that should exist." Records that were cut off from the file — even though they're still valid on the SIS side — get disabled or purged along with anything genuinely removed. A failed `store` simply fails to apply that batch; a truncated `refresh` can silently and incorrectly disable real, active records.

**Blackboard's strong recommendation:** limit `refresh` usage, and build feeds that limit unnecessary processing generally — favor sending only what actually changed over resubmitting a full population every cycle. `store` is the safer default: it only performs inserts and updates for the records explicitly present in the file, and never disables or purges anything the file doesn't mention — so a partial or truncated `store` file just under-applies that run's changes, rather than silently disabling records it never got to. Reserve `refresh` for cases where you specifically need Learn to reconcile away anything missing from the file, and treat it as the higher-risk operation it is — see the [Pre-Flight Checklist](#pre-flight-checklist) above and budget the process integrity safeguards (verified complete transfers, file validation, dry-runs) accordingly.

---

## Checking Processing Status

```text
GET https://{learn-host}/webapps/bb-data-integration-flatfile-{deployment-id}/endpoint/dataSetStatus/{dataSetUid}
```

Pass the `dataSetUid` from the POST response (see [Response Format](#response-format) above). This may be called well after the original POST completes — processing is asynchronous. Returns an XML block:

```xml
<dataSetStatus>
    <completedCount>5</completedCount>
    <dataIntegrationId type="blackboard.platform.dataintegration.DataIntegration">_123_1</dataIntegrationId>
    <dataSetUid>afc3d6e84df84f51944a06cccee8f59a</dataSetUid>
    <errorCount>0</errorCount>
    <lastEntryDate>2013-03-20T10:45:48-05:00</lastEntryDate>
    <queuedCount>0</queuedCount>
    <startDate>2013-03-20T10:45:48-05:00</startDate>
    <warningCount>0</warningCount>
</dataSetStatus>
```

`errorCount` and `warningCount` above zero mean some records did not process cleanly even though the original POST returned success — use these counts to detect a problem, then check the integration logs through the Administrator Panel UI for the specifics.

---

## Credential Handling

The shared username/password is a standing credential against a production system — treat it accordingly:

- **Never commit credentials** to this or any repository, and never paste them into a request pasted into chat, a ticket, or a log.
- **Pass credentials via environment variables** at invocation time (`SNAPSHOT_USERNAME`, `SNAPSHOT_PASSWORD` above), sourced from a secrets manager or a local `.env` file that is `.gitignore`d — not typed as literals in a command.
- **Keep credentials out of shell history.** Exporting them from a sourced file (rather than typing `curl -u user:pass ...` inline) avoids them landing in `.bash_history` / `.zsh_history`.
- **Scope credentials to a single Data Source Key** where your Learn configuration allows it, rather than sharing one integration-wide credential across unrelated feeds.
- **Redact from CI/automation logs.** If these requests run from a script or pipeline, make sure the runner doesn't echo the command line (which would include the Basic Auth header) into build logs.
- **Rotate periodically**, and immediately if a credential may have been exposed (chat, screenshare, log, etc.).

---

## Worked Examples

### Store — new/updated Users

```bash
export LEARN_HOST="learn.example.edu"
export DEPLOYMENT_ID="xxxxxxxxxxxxxxxx"
export SNAPSHOT_USERNAME="svc_snapshot"
export SNAPSHOT_PASSWORD="<from secrets manager>"

curl -w "\n%{http_code}\n" \
  -H "Content-Type: text/xml" \
  -u "${SNAPSHOT_USERNAME}:${SNAPSHOT_PASSWORD}" \
  --data-binary @./users_batch.txt \
  "https://${LEARN_HOST}/webapps/bb-data-integration-flatfile-${DEPLOYMENT_ID}/endpoint/person/store"
```

`users_batch.txt` follows the field layout in [User](../specs/snapshot-user.md), e.g.:

```text
external_person_key|data_source_key|firstname|lastname|user_id|email|available_ind|row_status
STU-100042|SIS-IMPORT-2025|Maria|Santos|msantos|msantos@university.edu|Y|enabled
```

### Complete Refresh — Courses (use with caution)

`refresh` will disable any course managed by this integration that is *not* in the submitted file — confirm the file is a full, current export before running this.

```bash
curl -w "\n%{http_code}\n" \
  -H "Content-Type: text/xml" \
  -u "${SNAPSHOT_USERNAME}:${SNAPSHOT_PASSWORD}" \
  --data-binary @./courses_full_export.txt \
  "https://${LEARN_HOST}/webapps/bb-data-integration-flatfile-${DEPLOYMENT_ID}/endpoint/course/refresh"
```

See [Course / Organization](../specs/snapshot-course.md) for the required field layout.

---

## Automating Requests

Don't just cron a raw `curl` call for a recurring feed (e.g. a nightly SIS export) — a reliable automation needs a dispatch step, a posting-and-status-polling step, archiving, and separate scheduling for `store` vs. `refresh`, at minimum.

For the full pattern — plus the option of subscribing to Blackboard's own SIS Framework Controller instead of building this yourself — see **[Automating Snapshot Feeds — Building a Controller](snapshot-automation-guide.md)**.

---

## Notes

- This guide covers the request mechanics only. Object-specific fields, required columns, and value formats live in each object's spec page linked from [`specs/README.md`](../specs/README.md).
- For recurring/scheduled feeds, see [Automating Snapshot Feeds — Building a Controller](snapshot-automation-guide.md).
- If your endpoint or Learn version behaves differently from what's described here (response format, status codes, auth scheme), trust your own instance's observed behavior over this document and update it accordingly.
