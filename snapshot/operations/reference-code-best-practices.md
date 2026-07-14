---
title: "Snapshot Flat File — Working with the Reference Code and Status Endpoint"
id: snapshot-reference-code-best-practices
categories: SIS, Snapshot Flat File
published: "2026-07-14"
edited: "2026-07-14"
author: "Jeff Kelley, Principal Solutions Engineer, Blackboard Inc."
---

# Working with the Reference Code and Status Endpoint

Every Snapshot Flat File POST that Learn accepts hands back a reference code — the `dataSetUid` — and a companion REST endpoint, `dataSetStatus`, that resolves that code to a processing outcome. This doc collects best practices for using both well. It assumes you're already familiar with the request/response mechanics in [Posting Requests](snapshot-posting-guide.md); start there for the request format itself.

> As with the rest of this repository, this content is provided for reference and educational purposes only, without support, maintenance, or warranty of any kind. Always confirm current behavior against your own Learn instance and Blackboard's official documentation before relying on it.

---

## What the Reference Code Represents

A 2xx POST response only confirms that Learn *accepted* a file for processing — Snapshot Flat File processing is asynchronous, so acceptance and completion are two different events, separated by however long the data set takes to process. The `dataSetUid` is the only thing that ties those two events together:

```text
Success: Feed File Uploaded. Use the reference code afc3d6e84df84f51944a06cccee8f59a to track these records in the logs.
```

Without it, there is no way to go back and ask Learn "what happened to the file I sent at 2am?" — so it's worth treating deliberately rather than as a value to glance at and discard.

---

## Best Practice: Capture and Record the Reference Code Immediately

Pull the `dataSetUid` out of the response body as part of the same step that sends the request — don't rely on being able to find it later in terminal scrollback or a mail notification.

Record it next to the metadata that gives it meaning: timestamp, target host, object, operation, and source filename. A single log line or row is enough:

```text
2026-07-14T02:00:04Z | learn.example.edu | person | store | users_batch.txt | afc3d6e84df84f51944a06cccee8f59a
```

Where this lives — a flat log file, a database table, a ticketing system comment — matters less than that it's durable and searchable later, and that it's written at submission time rather than reconstructed after the fact.

---

## Best Practice: Treat `dataSetStatus` as an Integration-Facing REST Endpoint

`dataSetStatus` is a plain `GET` that returns structured XML — it's built to be called by code, not just checked by a person in a browser or the Administrator Panel:

```text
GET https://{learn-host}/webapps/bb-data-integration-flatfile-{building-block-id}/endpoint/dataSetStatus/{dataSetUid}
```

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

Build the call into whatever submits the file in the first place, rather than leaving verification as a separate manual step:

- A one-off manual `store` can poll inline and print the final result before the script exits.
- A scheduled feed (see [Automating Requests](snapshot-posting-guide.md#automating-requests)) can poll as part of the per-file posting step, and use the result to decide whether to alert, retry, or continue to the next file.

Either way, the same endpoint serves both the "did my one-off change work?" case and the "did tonight's automated run work?" case — it doesn't need a different integration path for each.

---

## Best Practice: Poll to Completion, Not Just Once

`queuedCount` draining to zero is what indicates processing has actually finished. Checking `errorCount` and `warningCount` before that point can read as clean simply because Learn hasn't gotten to the failing records yet. A simple poll loop — wait, check `queuedCount`, repeat until zero, then read the final counts — is enough; there's no need for anything fancier than a bounded retry with backoff.

---

## Best Practice: Record the Outcome, Not Just the Request

The entry you wrote down in step one (timestamp, host, object, operation, filename, `dataSetUid`) is only half a record until it's paired with what `dataSetStatus` eventually reported:

```text
2026-07-14T02:00:04Z | learn.example.edu | person | store | users_batch.txt | afc3d6e84df84f51944a06cccee8f59a | completed=42 error=0 warning=1
```

A log that only shows what was *sent* can't answer "did it work?" without someone going back and re-polling a `dataSetUid` that may no longer be worth querying. A log that also shows what was *reported* answers that question by itself, and gives you a running history to check for patterns (e.g., the same object consistently producing warnings) without digging through the Administrator Panel each time.

---

## Best Practice: Use the Recorded Reference Code When Escalating

When a data set's `errorCount` or `warningCount` comes back above zero, `dataSetStatus` tells you *that* something didn't process cleanly but not *what* — that detail lives in the integration logs in the Administrator Panel, keyed by the same `dataSetUid`.

The same applies to opening a support case with Blackboard: leading with the `dataSetUid`, the host, and the approximate submission time lets support locate the batch in server-side logs directly, rather than having the request reconstructed from a description of symptoms.

---

## Notes

- This doc covers the reference code and status endpoint specifically. For the request/response mechanics of posting a file, see [Posting Requests](snapshot-posting-guide.md). For field-level object specs, see [`specs/`](../specs/README.md).
- If your endpoint or Learn version behaves differently from what's described here (response format, field names, retention of a `dataSetUid` over time), trust your own instance's observed behavior over this document and update it accordingly.
