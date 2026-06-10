---
title: "Snapshot Flat File — Subject to Organization Association"
id: snapshot-flatfile-subject-to-organization-association
categories: SIS, Snapshot Flat File
published: "2026-04-22"
edited: "2026-04-22"
author: "Jeff Kelley, Principal Solutions Engineer, Blackboard Inc."
---

# Subject to Organization Association

**SIS Object:** Subject to Organization Association  
**Endpoint:** `/endpoint/subjecttoorgassociation/`  
**Insert/Update behavior:** Smart Insert or Update  
**Delete behavior:** Disable

The Subject to Organization Association object links Organizations to Subjects, classifying organization offerings under their curricular subject area.

---

## Endpoints

| Operation | URL |
| :--- | :--- |
| Store | `.../endpoint/subjecttoorgassociation/store` |
| Complete Refresh | `.../endpoint/subjecttoorgassociation/refresh` |
| Complete Refresh by Data Source | `.../endpoint/subjecttoorgassociation/refreshlegacy` |
| Delete | `.../endpoint/subjecttoorgassociation/delete` |

---

## Fields

| Field | Header | Required | Unique | Format / Values / Max | Comments |
| :--- | :--- | :---: | :---: | :--- | :--- |
| Batch Uid | `external_association_key` | Yes | Yes | Max 64 | Unique identifier for this Subject-to-Organization association. Recommended convention: concatenate the Subject and Organization batch UIDs (e.g. `CHEM-SUBJ_ChemClub`). Use a natural unique key from your source system if one exists. |
| Data Source Key | `data_source_key` | Yes | No | Max 256, multi-byte | May be supplied by the integration configuration rather than the file. |
| Organization Batch Uid | `external_org_key` | Yes | No | Max 64 | The `external_organization_key` of the Organization being associated with the Subject. |
| Subject Batch Uid | `external_subject_key` | Yes | No | Max 64 | The `external_subject_key` of the Subject to which the Organization is being associated. |

---

## Sample Feed File

Header row is required. Column order is flexible. Values are pipe-delimited.

```text
external_association_key|data_source_key|external_subject_key|external_org_key
CHEM-SUBJ_ChemClub|SIS-IMPORT-2025|CHEM-SUBJ|ChemClub
```

---

## Notes

- **Minimum required headers:** `external_association_key`, `data_source_key`, `external_org_key`, `external_subject_key`.
- **`external_association_key`** must be unique. The recommended convention is to concatenate the Subject and Organization batch UIDs. If your source system has a natural unique key, that may be used instead.
- **Both the Subject and Organization must already exist** before creating this association.
