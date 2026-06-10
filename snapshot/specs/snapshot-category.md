---
title: "Snapshot Flat File — Category"
id: snapshot-flatfile-category
categories: SIS, Snapshot Flat File
published: "2026-04-22"
edited: "2026-04-22"
author: "Jeff Kelley, Principal Solutions Engineer, Blackboard Inc."
---

# Category

**SIS Object:** Course / Organization Category  
**Endpoint:** `/endpoint/coursecategory/`  
**Insert/Update behavior:** Smart Insert or Update  
**Delete behavior:** Disable

The Category object creates and manages catalog categories for Courses and Organizations. Categories may be hierarchical — a category can be the parent of other categories.

---

## Endpoints

| Operation | URL |
| :--- | :--- |
| Store (Course Category) | `.../endpoint/coursecategory/coursecategory/store` |
| Complete Refresh (Course Category) | `.../endpoint/coursecategory/coursecategory/refresh` |
| Complete Refresh by Data Source (Course Category) | `.../endpoint/coursecategory/coursecategory/refreshlegacy` |
| Delete (Course Category) | `.../endpoint/coursecategory/coursecategory/delete` |
| Store (Organization Category) | `.../endpoint/coursecategory/organizationcategory/store` |
| Complete Refresh (Organization Category) | `.../endpoint/coursecategory/organizationcategory/refresh` |
| Complete Refresh by Data Source (Organization Category) | `.../endpoint/coursecategory/organizationcategory/refreshlegacy` |
| Delete (Organization Category) | `.../endpoint/coursecategory/organizationcategory/delete` |

---

## Fields

| Field | Header | Required | Unique | Format / Values / Max | Comments |
| :--- | :--- | :---: | :---: | :--- | :--- |
| Batch Uid | `external_category_key` | Yes | Yes | Max 64, multi-byte | Must be unique. Corresponds to the Category Mnemonic field in the UI. |
| Data Source Key | `data_source_key` | Yes | No | Max 256, multi-byte | May be supplied by the integration configuration rather than the file. |
| Title | `title` | Yes | No | Max 255, multi-byte | The name of the category as displayed to users in the UI. |
| Available | `available_ind` | No | No | `Y` \| `N` | Establishes availability within Blackboard Learn. |
| Description | `description` | No | No | — | Category description. |
| Front Page | `frontpage_ind` | No | No | `Y` \| `N` | Determines whether the category is displayed on the front page of the catalog. |
| Is Restricted | `restrict_ind` | No | No | `Y` \| `N` | Restricts the Course or Organization to members only. |
| Parent Batch Uid | `parent_category_key` | No | No | Max 64 | The `external_category_key` of the parent category. Makes this category a child of the specified parent. |
| Replacement Batch Uid | `new_external_category_key` | No | Yes | Max 64, multi-byte | Use only when the category's EXTERNAL KEY must change. |
| Replacement Data Source Batch Uid | `new_data_source_key` | No | No | — | UI mapping: `script.flatfile.CourseCatReplacementDataSourceBatchUid` |
| Row Status | `row_status` | No | No | `enabled` \| `disabled` \| `deleted` | `enabled`: normal access. `disabled`: visible but not editable. `deleted`: scheduled for removal. |

---

## Sample Feed File

Header row is required. Column order is flexible. Values are pipe-delimited.

```text
external_category_key|data_source_key|title|available_ind|frontpage_ind|row_status
CAT-STEM|SIS-IMPORT-2025|STEM Courses|Y|Y|enabled
```

---

## Notes

- **Course and Organization categories use the same fields** but are submitted to separate endpoints (`/coursecategory/` or `/organizationcategory/`).
- **`parent_category_key`** must reference an existing category. Submit parent categories before child categories.
