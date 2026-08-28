---
title: "Automating Snapshot Feeds — Building a Controller"
id: snapshot-flatfile-automation-guide
categories: SIS, Snapshot Flat File
version: "1.0"
published: "2026-08-28"
edited: "2026-08-28"
author: "Jeff Kelley, Principal Solutions Engineer, Blackboard Inc."
---

# Automating Snapshot Feeds — Building a Controller

> **v1.0 — work in progress.** This guide is newer and less battle-tested than the rest of this repo's operational docs; the shape of the guidance is solid but expect gaps and revisions as it gets used against real controller builds.

Guidance for turning one-off Snapshot Flat File requests (see [Posting Requests](snapshot-posting-guide.md)) into a reliable, recurring, unattended feed — plus what to weigh before deciding to build that automation yourself versus subscribing to a managed one.

> As with the rest of this repository, this content is provided as-is, without warranty or support of any kind — Blackboard retains all rights. Always confirm current behavior against your own Learn instance and Blackboard's official documentation before relying on it.

---

## In Plain Terms

Sending one file by hand is easy — you run a command, you get a receipt, you're done. A real SIS feed isn't one file, though; it's dozens of files, every night, forever, in a specific order, with someone (or something) checking that each one actually landed correctly and doing something sensible when one doesn't.

A **controller** is the piece of software that does that watching and checking for you, instead of a person running commands by hand at 2am. It's a separate thing from the **generator** — the client-side process (part of the SIS, a nightly export job, a middleware layer) that actually creates the flat files and delivers them somewhere the controller can reach. The controller doesn't produce data; it takes whatever the generator hands it and gets it into Learn reliably. This guide describes what a controller needs to do, so you can either build a small one yourself or evaluate whether to let Blackboard run one for you.

---

## What a Controller Does

At minimum, a controller needs to handle five jobs. This repo doesn't vendor a reference implementation — treat this as the shape to replicate, using the request mechanics from the [Posting Requests](snapshot-posting-guide.md) guide as the building block for the "post a file" step.

### 1. Intake / Dispatch

Checks a drop location (a directory, an SFTP folder, a queue — wherever the generator writes files) for new files, and figures out what each one is and where it needs to go. In principle this could run continuously, watching the drop location for anything new — but in practice it's more common, and simpler, to run intake on a schedule coordinated with the generator (e.g. the generator finishes its export by 1am, so intake runs at 1:30am) rather than build and maintain a true watch process.

- Determine each file's object type (`person`, `course`, `membership`, etc.) before dispatching it. Matching against a filename convention (e.g. `users_YYYYMMDD.txt`) is the more common approach in practice, and slightly easier to implement, but it's only as reliable as the naming discipline of whatever produces the file. Inspecting the header row instead is more exact — it identifies the file by what's actually in it, not what it's called — at the cost of a bit more dispatch logic.
- Group and order files so dependencies are respected — **users, then courses, then memberships** is the typical order, since later objects reference earlier ones.
- Decide `store` vs. `refresh` per file (often driven by naming convention or drop-folder-per-operation), since the two should never share a schedule (see [Scheduling](#scheduling) below).

### 2. Posting

Does the actual HTTP POST for a single file, per the [Request Template](snapshot-posting-guide.md#request-template) in the posting guide, and captures the `dataSetUid` from the response.

This step should also work standalone — invoked manually for a one-off submission — not just as something the dispatcher calls.

### 3. Status Polling

Polls the [`dataSetStatus`](snapshot-posting-guide.md#checking-processing-status) endpoint until the data set finishes processing, then checks `errorCount` and `warningCount`, not just that the POST returned a 2xx. A file can be accepted and still fail to process cleanly.

### 4. Archiving

Once a file's status confirms completion, move it out of the drop location (e.g. append a processing timestamp and relocate it) before the dispatcher considers the next file. This keeps a re-run of the dispatcher from re-submitting a file that already succeeded, and gives you an audit trail of what was actually sent.

### 5. Reporting & Alerting

Send a summary after each batch — files processed, records completed/errored/warned per file — to whoever owns the integration, and alert loudly (not just log quietly) when `errorCount` is nonzero or a file fails outright. A controller that fails silently is worse than no automation at all, since it creates false confidence that the feed is current.

---

## Scheduling

- **Coordinate the intake schedule with the generator, not just with itself.** If the generator's export slips (runs late, retries, fails partway) and intake fires on a fixed clock time regardless, it can pick up a partial or stale file. Build in a buffer after the generator's expected finish time, and where possible have intake confirm the generator actually completed (a marker/done file, a status check) before it starts.
- **Never share a schedule between `store` and `refresh`.** Refresh operations process the full managed set and can run substantially longer than a store of similar file size — see the [Pre-Flight Checklist](snapshot-posting-guide.md#pre-flight-checklist) in the posting guide. Give each its own cron entry (and drop location, if dispatch is directory-per-operation) so a slow refresh doesn't collide with the next scheduled store.
- Build in enough margin between scheduled runs that a slow run has room to finish before the next one starts, and alert if a run is still active when the next one would normally begin.

---

## Other Things a Controller Needs to Get Right

- **Credential handling.** Same rules as manual posting apply, only more so, since a controller runs unattended: see [Credential Handling](snapshot-posting-guide.md#credential-handling) in the posting guide — environment/secrets-manager sourcing, no literals in scripts or logs, scoped credentials, rotation.
- **Retries.** Distinguish a transient failure (network blip, momentary 5xx) worth retrying from a real rejection (malformed file, bad auth) that will just fail again — retrying the latter in a loop wastes time and can obscure the real problem in alert noise.
- **Idempotency awareness.** `store` is safe to re-run. `refresh` and `delete` are not something you want a retry loop firing twice by accident — see [Delete Behaviors](../snapshot-flat-file-overview.md#delete-behaviors).
- **Environment separation.** Make it hard to point a production controller config at a test host or vice versa — see the first item in the [Pre-Flight Checklist](snapshot-posting-guide.md#pre-flight-checklist).

---

## Build vs. Buy: The SIS Framework Controller

Everything above is buildable in-house — most institutions running Snapshot at scale end up with something like it, whether it's a purpose-built script, a workflow in an existing automation platform, or a scheduled job in their SIS integration layer. Building it yourself gives you full control over the intake logic, scheduling, and reporting format, but it also means your team owns the ongoing maintenance: keeping up with object/endpoint changes, monitoring the automation itself, and handling on-call when a nightly run fails.

Blackboard also offers the **SIS Framework Controller**, a subscription-based Blackboard/Platform Extension that provides a managed controller for Snapshot Flat File feeds — intake, posting, status polling, and reporting handled as a supported product rather than custom code your team maintains.

This repo doesn't include product documentation for the SIS Framework Controller — it's a separate, licensed offering, not something covered by these open reference materials. If a managed controller is a better fit than building one, talk to your Blackboard/Anthology account team about availability and current capabilities.

---

## Notes

- This guide describes the pattern; it isn't a reference implementation. The actual object-processing order and per-object payloads should come from this repo's [object specs](../specs/README.md).
- For a closely related official reference, see Blackboard's [Snapshot Flat File Automation](https://help.anthology.com/blackboard/administrator/en/integrations/student-information-system--sis-/snapshot-flat-file/snapshot-flat-file-automation.html) guide.
- If your endpoint or Learn version behaves differently from what's described here, trust your own instance's observed behavior over this document and update it accordingly.
