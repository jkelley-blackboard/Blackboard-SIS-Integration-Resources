# Snapshot Flat File

This section contains resources for the Blackboard Learn Snapshot Flat File integration type.

> This content is provided as-is, without warranty or support of any kind. Blackboard retains all rights. Use at your own risk.

For an introduction to the integration type, file format, and a full index of supported objects, start here:

**[Snapshot Flat File — Overview](snapshot-flat-file-overview.md)**

---

## Contents

### [`specs/`](specs/)
Field-level specifications for all Snapshot Flat File object types, in Markdown format.

### [`operations/`](operations/)
Guidance for running the integration day-to-day: [Posting Requests](operations/snapshot-posting-guide.md) covers how to construct and send the HTTP requests and check processing status; [Automating Snapshot Feeds](operations/snapshot-automation-guide.md) covers turning that into a reliable recurring feed, including build-vs-buy against Blackboard's subscription SIS Framework Controller; [Converting Full-Load Exports to Diffs](operations/snapshot-diff-guide.md) covers replacing full-load `refresh` posts with a smaller, safer changes-only feed.

### [`tools/`](tools/)
Scripts for working with Snapshot flat files, starting with [`validate_snapshot_files.py`](tools/validate_snapshot_files.py) — validates a folder of flat-file CSV exports against the specs in `specs/`.
