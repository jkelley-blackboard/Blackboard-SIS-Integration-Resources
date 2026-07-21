---
title: "Snapshot Flat File — Course / Organization Membership"
id: snapshot-flatfile-membership
categories: SIS, Snapshot Flat File
published: "2026-04-22"
edited: "2026-07-21"
author: "Jeff Kelley, Principal Solutions Engineer, Blackboard Inc."
---

# Course / Organization Membership

**SIS Object:** Course or Organization Memberships (Enrollments and Staff Assignments)  
**Endpoint:** `/endpoint/membership/`  
**Insert/Update behavior:** Smart Insert or Update  
**Delete behavior:** Disable

The Membership object creates and manages enrollments and staff assignments for Courses and Organizations. Courses and Organizations use the same fields but are submitted to separate endpoints.

---

## Endpoints

| Operation | URL |
| :--- | :--- |
| Store (Course) | `.../endpoint/membership/membership/store` |
| Complete Refresh (Course) | `.../endpoint/membership/membership/refresh` |
| Complete Refresh by Data Source (Course) | `.../endpoint/membership/membership/refreshlegacy` |
| Delete (Course) | `.../endpoint/membership/membership/delete` |
| Store (Organization) | `.../endpoint/membership/organizationmembership/store` |
| Complete Refresh (Organization) | `.../endpoint/membership/organizationmembership/refresh` |
| Complete Refresh by Data Source (Organization) | `.../endpoint/membership/organizationmembership/refreshlegacy` |
| Delete (Organization) | `.../endpoint/membership/organizationmembership/delete` |

---

## Fields

| Field | Header | Required | Unique | Format / Values / Max | Comments |
| :--- | :--- | :---: | :---: | :--- | :--- |
| Course / Org Batch Uid | `external_course_key` | Yes | No | Max 64, multi-byte | Use `external_organization_key` for Organizations. |
| Data Source Key | `data_source_key` | Yes | No | Max 256, multi-byte | May be supplied by the integration configuration rather than the file. |
| User Batch Uid | `external_person_key` | Yes | No | Max 64, multi-byte | The `external_person_key` of the user being enrolled. |
| Role | `role` | No | No | `Instructor` \| `teaching_assistant` \| `course_builder` \| `Grader` \| `Student` \| `guest` \| `none` | The user's role in the Course. |
| Available | `available_ind` | No | No | `Y` \| `N` | Establishes availability within Blackboard Learn. |
| Availability Override Date | `bypass_date` | No | No | Date, exact format not yet confirmed | Field Mapping label: "Availability Override Date". Maps to SIS field `flatFileMemberBypassDate`. Purpose/behavior not yet confirmed against a live Create/Edit page. |
| Row Status | `row_status` | No | No | `enabled` \| `disabled` \| `deleted` | `enabled`: normal access. `disabled`: visible but not editable. `deleted`: scheduled for removal. |
| Cartridge Access | `cartridge_ind` | No | No | — | **Deprecated.** Header exists for legacy file compatibility but has no corresponding Field Mapping row — cannot be configured in the GUI. Do not use. |
| Image URL | `photo_link` | No | No | — | **Deprecated.** Not displayed or used anywhere in the application, despite still being field-mappable in the GUI (maps to SIS field `flatFileMemberPhotoLink`). |
| Include In Roster | `roster_ind` | No | No | `Y` \| `N` | Flag indicating whether the user is displayed in the course roster. |
| Introduction | `intro` | No | No | Max 4000, multi-byte | **Deprecated.** Not displayed or used anywhere in the application. |
| Notes | `note` | No | No | No limit, multi-byte | **Deprecated.** Not displayed or used anywhere in the application. |
| Personal Information | `pinfo` | No | No | No limit, multi-byte | **Deprecated.** Not displayed or used anywhere in the application. |
| Primary Instructor | `primary_instructor` | No | No | `Y` \| `N` | Indicates primary instructor. Member must have a course role with the 'treat as instructor' flag. A `Y` value on a non-instructor role is rejected. |
| Receive Email | `receive_email_ind` | No | No | `Y` \| `N` | Flag whether email is enabled for this user in this course. |
| Replacement Data Source Batch Uid | `new_data_source_key` | No | No | — | Field Mapping label: "Membership Replacement Data Source Batch Uid" (internal name `flatFileMemberReplacementDataSourceBatchUid`). |
| Website 1 — Description | `link_desc_1` | No | No | Max 255 | **Deprecated.** Not displayed or used anywhere in the application. |
| Website 1 — Name | `link_name_1` | No | No | Max 100 | **Deprecated.** Not displayed or used anywhere in the application. |
| Website 1 — URL | `link_url_1` | No | No | Max 100 | **Deprecated.** Not displayed or used anywhere in the application. |
| Website 2 — Description | `link_desc_2` | No | No | Max 255 | **Deprecated.** Not displayed or used anywhere in the application. |
| Website 2 — Name | `link_name_2` | No | No | Max 100 | **Deprecated.** Not displayed or used anywhere in the application. |
| Website 2 — URL | `link_url_2` | No | No | Max 100 | **Deprecated.** Not displayed or used anywhere in the application. |
| Website 3 — Description | `link_desc_3` | No | No | Max 255 | **Deprecated.** Not displayed or used anywhere in the application. |
| Website 3 — Name | `link_name_3` | No | No | Max 100 | **Deprecated.** Not displayed or used anywhere in the application. |
| Website 3 — URL | `link_url_3` | No | No | Max 100 | **Deprecated.** Not displayed or used anywhere in the application. |

---

## Sample Feed File

Header row is required. Column order is flexible. Values are pipe-delimited.

```text
external_course_key|data_source_key|external_person_key|role|available_ind|row_status
MATH101-F25|SIS-IMPORT-2025|STU-100042|Student|Y|enabled
```

---

## Notes

- **Course and Organization memberships use the same fields** but different endpoints and key headers (`external_course_key` vs `external_organization_key`).
- **`primary_instructor`** is only valid for course roles that have the 'treat as instructor' flag enabled. A `Y` value on any other role type is silently rejected.
- **Several fields are deprecated — non-functional and not displayed anywhere in the application — despite still being configurable in Field Mapping:** `cartridge_ind` (Cartridge Access), `photo_link` (Image URL), `intro` (Introduction), `note` (Notes), `pinfo` (Personal Information), and all Website fields (`link_name_1/2/3`, `link_url_1/2/3`, `link_desc_1/2/3`). Remove these from any existing feeds.
- **The Field Mapping page also lists "Batch Uid," "Replacement Batch Uid," "Course ID," and "Move Cross-listed Enrollment"** as Learn Enrollments fields — "Batch Uid" shows its source as "Membership External Key." This is misleading: Blackboard Learn has no actual membership batch UID / external key concept, and none of these four fields appear anywhere in the Header Override list, meaning none of them can be populated from the flat file at all. Treat "Membership External Key" as an internal Field Mapping page label, not a real header or a value you need to supply.
