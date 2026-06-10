---
title: "Snapshot Flat File — Hierarchy Node"
id: snapshot-flatfile-hierarchy-node
categories: SIS, Snapshot Flat File
published: "2026-04-22"
edited: "2026-04-22"
author: "Jeff Kelley, Principal Solutions Engineer, Blackboard Inc."
---

# Hierarchy Node

**SIS Object:** Hierarchy Node  
**Endpoint:** `/endpoint/node/`  
**Insert/Update behavior:** Smart Insert or Update  
**Delete behavior:** Purge

The Hierarchy Node object creates and manages nodes in the Institutional Hierarchy. Nodes are organized into a tree structure with a required parent reference.

---

## Endpoints

| Operation | URL |
| :--- | :--- |
| Store | `.../endpoint/node/store` |
| Complete Refresh | `.../endpoint/node/refresh` |
| Complete Refresh by Data Source | `.../endpoint/node/refreshlegacy` |
| Delete | `.../endpoint/node/delete` |

---

## Fields

| Field | Header | Required | Unique | Format / Values / Max | Comments |
| :--- | :--- | :---: | :---: | :--- | :--- |
| Batch Uid | `external_node_key` | Yes | Yes | Max 255, multi-byte | Letters, digits, dashes, and periods only — no spaces. |
| Data Source Key | `data_source_key` | Yes | No | Max 256, multi-byte | May be supplied by the integration configuration rather than the file. |
| Parent Batch Uid | `parent_node_key` | Yes | No | Max 64 | The `external_node_key` of the parent node. Submit parent nodes before child nodes. |
| Name | `name` | Yes | No | Max 255 | Node name as displayed in the UI. |
| Description | `description` | No | No | Max 1000 | Description of the node. |
| Replacement Batch Uid | `new_external_node_key` | No | Yes | Max 255, multi-byte | Use only when a Node's EXTERNAL KEY must change. |
| Replacement Data Source Batch Uid | `new_data_source_key` | No | No | — | UI mapping: `script.flatfile.NodeReplacementDataSourceBatchUid` |

---

## Sample Feed File

Header row is required. Column order is flexible. Values are pipe-delimited.

```text
external_node_key|data_source_key|parent_node_key|name
NODE.ENGR.DEPT|SIS-IMPORT-2025|NODE.ENGR|Department of Engineering
```

---

## Notes

- **Delete behavior is Purge.** Deleted nodes are permanently removed.
- **Minimum required headers:** `external_node_key`, `data_source_key`, `parent_node_key`, `name`.
- **Submit parent nodes before child nodes** to ensure the hierarchy can be resolved.
- **`external_node_key`** may contain only letters, digits, dashes, and periods — no spaces.
