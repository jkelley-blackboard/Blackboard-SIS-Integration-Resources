---
title: "Snapshot Flat File — Program to Subject Association"
id: snapshot-flatfile-program-to-subject-association
categories: SIS, Snapshot Flat File
published: "2026-04-22"
edited: "2026-04-22"
author: "Jeff Kelley, Principal Solutions Engineer, Blackboard Inc."
---

# Program to Subject Association

**SIS Object:** Program to Subject Association  
**Endpoint:** `/endpoint/programtosubjectassociation/`  
**Insert/Update behavior:** Smart Insert or Update  
**Delete behavior:** Disable

The Program to Subject Association object links Subjects to Programs, establishing the curricular relationship between a degree program and its constituent subject areas.

---

## Endpoints

| Operation | URL |
| :--- | :--- |
| Store | `.../endpoint/programtosubjectassociation/store` |
| Complete Refresh | `.../endpoint/programtosubjectassociation/refresh` |
| Complete Refresh by Data Source | `.../endpoint/programtosubjectassociation/refreshlegacy` |
| Delete | `.../endpoint/programtosubjectassociation/delete` |

---

## Fields

| Field | Header | Required | Unique | Format / Values / Max | Comments |
| :--- | :--- | :---: | :---: | :--- | :--- |
| Batch Uid | `external_association_key` | Yes | Yes | Max 64 | Unique identifier for this Program-to-Subject association. Recommended convention: concatenate the Program and Subject batch UIDs (e.g. `PROG-BSCS_CHEM-SUBJ`). Use a natural unique key from your source system if one exists. |
| Data Source Key | `data_source_key` | Yes | No | Max 256, multi-byte | May be supplied by the integration configuration rather than the file. |
| Program Batch Uid | `external_program_key` | Yes | No | Max 64 | The `external_program_key` of the Program to which the Subject is being associated. |
| Subject Batch Uid | `external_subject_key` | Yes | No | Max 64 | The `external_subject_key` of the Subject being associated with the Program. |

---

## Sample Feed File

Header row is required. Column order is flexible. Values are pipe-delimited.

```text
external_association_key|data_source_key|external_program_key|external_subject_key
PROG-BSCS_CHEM-SUBJ|SIS-IMPORT-2025|PROG-BSCS|CHEM-SUBJ
```

---

## Notes

- **Minimum required headers:** `external_association_key`, `data_source_key`, `external_program_key`, `external_subject_key`.
- **`external_association_key`** must be unique. The recommended convention is to concatenate the Program and Subject batch UIDs. If your source system has a natural unique key, that may be used instead.
- **Both the Program and Subject must already exist** before creating this association.
