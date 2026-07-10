---
title: "Snapshot Flat File — Posting Requests"
id: snapshot-flatfile-posting-guide
categories: SIS, Snapshot Flat File
published: "2026-07-10"
edited: "2026-07-10"
author: "Jeff Kelley, Principal Solutions Engineer, Blackboard Inc."
---

# Posting Requests

Operational guidance for constructing and executing the HTTP requests that submit Snapshot Flat File data to Blackboard Learn. This complements the field-level object specs — start there for file format and required fields per object; use this doc when you're ready to actually send a request.

> As with the rest of this repository, this content is provided for reference and educational purposes only, without support, maintenance, or warranty of any kind. Always confirm current behavior against your own Learn instance and Blackboard's official documentation before relying on it.

---

## Request Template

Every Snapshot Flat File request is an HTTPS POST with HTTP Basic Auth and the file as the raw request body.

```text
POST https://{learn-host}/webapps/bb-data-integration-flatfile-{building-block-id}/endpoint/{object}/{operation}
Authorization: Basic base64(username:password)
Content-Type: text/xml
```

`curl` equivalent, parameterized:

```bash
curl -w "\n%{http_code}\n" \
  -H "Content-Type: text/xml" \
  -u "${SNAPSHOT_USERNAME}:${SNAPSHOT_PASSWORD}" \
  --data-binary @"${FILE_PATH}" \
  "https://${LEARN_HOST}/webapps/bb-data-integration-flatfile-${BB_ID}/endpoint/${OBJECT}/${OPERATION}"
```

- `{object}` — endpoint slug from the [Overview](snapshot-flat-file-overview.md#complete-endpoint-reference) table, e.g. `person`, `course`, `membership`.
- `{operation}` — `store`, `refresh`, `refreshlegacy`, or `delete`.
- `-k` (insecure/skip TLS verification) should only ever be used against a known test/sandbox host with a self-signed cert — never against production.
- `-w "%{http_code}"` surfaces the HTTP status code so a failed request isn't mistaken for success.

---

## Pre-Flight Checklist

Run through this before firing any request that isn't a `store` against a test environment:

1. **Confirm the target host.** Double-check `{learn-host}` resolves to the environment you intend (Test/Stage vs. Production). It's easy to fire a script at the wrong environment.
2. **Confirm the operation.** `store` is additive/idempotent (smart insert-or-update). `refresh` and `refreshlegacy` will disable or purge any record *not* present in the submitted file, scoped to the whole integration or a single Data Source Key respectively. `delete` acts only on records listed in the file. See the [Delete Behaviors](snapshot-flat-file-overview.md#delete-behaviors) table — some objects are purged, not disabled, and purge is not recoverable.
3. **Confirm the Data Source Key.** It must already exist in **Administrator Panel > Data Integration > Data Source Keys**, and must match what the file (or the integration config) expects. This matters most for `refreshlegacy`, which scopes the refresh to one key.
4. **Validate the file before sending.** Header row present, pipe-delimited, UTF-8, required columns per the relevant object spec. Sending a malformed file to `refresh` is more costly than to `store` since it defines "everything that should still exist."
5. **Dry-run on Test/Stage first** for anything other than a small `store` batch, if a non-production Learn instance is available to you.
6. **Check the response code and body**, not just "the command exited." A 2xx response acknowledges receipt — it does not by itself guarantee every record processed without error.
7. **Follow up on processing status.** Learn processes submitted data sets asynchronously; use the status endpoint below to confirm the batch actually completed and to check for per-record errors, rather than assuming success from the POST response alone.
8. **Log what you did** (host, object, operation, filename, timestamp, initiator) somewhere durable for audit purposes — but never log the credentials themselves.

---

## Checking Processing Status

```text
GET https://{learn-host}/webapps/bb-data-integration-flatfile-{building-block-id}/endpoint/dataSetStatus/{dataSetUid}
```

Use this to confirm a previously submitted data set finished processing and to check for per-record errors. Consult your Learn instance's response to a submission for how `{dataSetUid}` is surfaced — this varies by version/configuration, so verify it against your own environment rather than assuming a specific response shape.

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
export BB_ID="xxxxxxxxxxxxxxxx"
export SNAPSHOT_USERNAME="svc_snapshot"
export SNAPSHOT_PASSWORD="<from secrets manager>"

curl -w "\n%{http_code}\n" \
  -H "Content-Type: text/xml" \
  -u "${SNAPSHOT_USERNAME}:${SNAPSHOT_PASSWORD}" \
  --data-binary @./users_batch.txt \
  "https://${LEARN_HOST}/webapps/bb-data-integration-flatfile-${BB_ID}/endpoint/person/store"
```

`users_batch.txt` follows the field layout in [User](snapshot-user.md), e.g.:

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
  "https://${LEARN_HOST}/webapps/bb-data-integration-flatfile-${BB_ID}/endpoint/course/refresh"
```

See [Course / Organization](snapshot-course.md) for the required field layout.

---

## Notes

- This guide covers the request mechanics only. Object-specific fields, required columns, and value formats live in each object's spec page linked from [`specs/README.md`](README.md).
- If your endpoint or Learn version behaves differently from what's described here (response format, status codes, auth scheme), trust your own instance's observed behavior over this document and update it accordingly.
