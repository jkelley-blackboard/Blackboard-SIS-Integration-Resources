---
title: "Snapshot Flat File — Category Membership"
id: snapshot-flatfile-category-membership
categories: SIS, Snapshot Flat File
published: "2026-04-22"
edited: "2026-04-22"
author: "Jeff Kelley, Principal Solutions Engineer, Blackboard Inc."
---

# Category Membership

**SIS Object:** Course / Organization Category Membership  
**Endpoint:** `/endpoint/coursecategorymembership/`  
**Insert/Update behavior:** Smart Insert or Update  
**Delete behavior:** Disable

The Category Membership object associates Courses and Organizations with catalog categories.

---

## Endpoints

| Operation | URL |
| :--- | :--- |
| Store (Course) | `.../endpoint/coursecategorymembership/coursecategorymembership/store` |
| Complete Refresh (Course) | `.../endpoint/coursecategorymembership/coursecategorymembership/refresh` |
| Complete Refresh by Data Source (Course) | `.../endpoint/coursecategorymembership/coursecategorymembership/refreshlegacy` |
| Delete (Course) | `.../endpoint/coursecategorymembership/coursecategorymembership/delete` |
| Store (Organization) | `.../endpoint/coursecategorymembership/organizationcategorymembership/store` |
| Complete Refresh (Organization) | `.../endpoint/coursecategorymembership/organizationcategorymembership/refresh` |
| Complete Refresh by Data Source (Organization) | `.../endpoint/coursecategorymembership/organizationcategorymembership/refreshlegacy` |
| Delete (Organization) | `.../endpoint/coursecategorymembership/organizationcategorymembership/delete` |

---

## Fields

| Field | Header | Required | Unique | Format / Values / Max | Comments |
| :--- | :--- | :---: | :---: | :--- | :--- |
| Batch Uid | `(auto-populated)` | Yes | Yes | — | Auto-populated by the system. Do not include in data feeds. |
| Category Batch Uid | `external_category_key` | Yes | No | Max 64 | The `external_category_key` of the category to which to add the course or organization. |
| Course / Org Batch Uid | `external_course_key` | Yes | No | Max 64 | Use `external_organization_key` for Organizations. |
| Data Source Key | `data_source_key` | Yes | No | Max 256, multi-byte | May be supplied by the integration configuration rather than the file. |
| Available | `available_ind` | No | No | `Y` \| `N` | Establishes availability within Blackboard Learn. |
| Replacement Data Source Batch Uid | `new_data_source_key` | No | No | — | UI mapping: `script.flatfile.CourseCatMemReplacementDataSourceBatchUid` |
| Row Status | `row_status` | No | No | `enabled` \| `disabled` \| `deleted` | `enabled`: normal access. `disabled`: visible but not editable. `deleted`: scheduled for removal. |

---

## Sample Feed File

Header row is required. Column order is flexible. Values are pipe-delimited.

```text
external_category_key|external_course_key|data_source_key|available_ind|row_status
CAT-STEM|MATH101-F25|SIS-IMPORT-2025|Y|enabled
```

---

## Notes

- **Course and Organization category memberships use the same fields** but are submitted to separate endpoints (`/coursecategorymembership/` or `/organizationcategorymembership/`).
- **The Category and Course / Organization must already exist** before creating a membership.
