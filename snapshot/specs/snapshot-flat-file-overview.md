---
title: "Snapshot Flat File — Overview"
id: snapshot-flatfile-overview
categories: SIS, Snapshot Flat File
published: "2026-04-22"
edited: "2026-04-22"
author: "Jeff Kelley, Principal Solutions Engineer, Blackboard Inc."
---

# Snapshot Flat File — Field Reference Overview

The Snapshot Flat File integration type provides a flexible, file-based method for provisioning and managing data in Blackboard Learn. Structured data files are posted to HTTP endpoints to create, update, or delete Courses, Users, Enrollments, and related objects.

This reference documents all supported LEARN objects, their field specifications, and endpoint URLs.

---

## General File Format

- **File type:** Plain text, pipe-delimited (`|`)
- **Header row:** Required. Must be the first row of every file.
- **Column order:** Flexible — columns may appear in any order.
- **Character encoding:** UTF-8
- **All data types:** String. Numeric and date fields use specific formats as noted in each object's field table.
- **Custom header mapping:** Supported via the Snapshot Flat File Custom Header Mapping configuration. Allows existing file formats to be mapped to Blackboard field names without reformatting source files.

---

## Operation Types

Each endpoint supports four operation types:

| Operation | Path | Description |
| :--- | :--- | :--- |
| Store | `.../store` | Insert new records; update existing records. Default behavior is Smart Insert or Update. |
| Complete Refresh | `.../refresh` | Replace the full set of records managed by this integration with the contents of the submitted file. Records not present in the file are disabled or purged depending on the object type. |
| Complete Refresh by Data Source | `.../refreshlegacy` | Same as Complete Refresh but scoped to a specific Data Source Key. |
| Delete | `.../delete` | Disable or purge the records identified in the submitted file. |

---

## Data Source Keys

Every object requires a `data_source_key` that groups records for management purposes. The Data Source Key:

- Must be created in Blackboard Learn before use (**Administrator Panel > Data Integration > Data Source Keys**)
- May be supplied by the integration configuration, in which case it does not need to appear in the file
- Scopes Complete Refresh by Data Source operations to only the records associated with that key

---

## Delete Behaviors

| Behavior | Description | Objects |
| :--- | :--- | :--- |
| **Disable** | Record remains visible but is inaccessible. Can be re-enabled. | User, Course, Membership, Terms, Category, Subject, Program, Secondary Institution Role, Observer Association, Category Membership |
| **Purge** | Record is permanently removed and cannot be recovered. | Hierarchy Node, Hierarchy User Association, Hierarchy Course Association, Course Standard Association |

---

## LEARN Objects

The following objects are supported by the Snapshot Flat File integration. Five objects — Program, Program to Subject Association, Subject to Course Association, Subject to Organization Association, and Course Standard Association — support the Curricular Structure feature set and require Blackboard Learn's curricular structure features to be enabled.

### Core Objects

| Object | Endpoint Slug | SIS Object | Delete Behavior |
| :--- | :--- | :--- | :--- |
| [User](./snapshot-user.md) | `person` | Person | Disable |
| [Course / Organization](./snapshot-course.md) | `course` / `organization` | Course or Organization | Disable |
| [Course / Organization Membership](./snapshot-membership.md) | `membership` / `organizationmembership` | Enrollments & Staff Assignments | Disable |
| [Terms](./snapshot-terms.md) | `term` | Term | Disable |

### Roles & Associations

| Object | Endpoint Slug | SIS Object | Delete Behavior |
| :--- | :--- | :--- | :--- |
| [Secondary Institution Role](./snapshot-secondary-institution-role.md) | `secondaryinstrole` | User Secondary Institution Role | Disable |
| [Observer Association](./snapshot-observer-association.md) | `associateobserver` | Observer Association | Disable |

### Catalog

| Object | Endpoint Slug | SIS Object | Delete Behavior |
| :--- | :--- | :--- | :--- |
| [Category](./snapshot-category.md) | `coursecategory` / `organizationcategory` | Course / Org Category | Disable |
| [Category Membership](./snapshot-category-membership.md) | `coursecategorymembership` / `organizationcategorymembership` | Course / Org Category Membership | Disable |

### Curricular Structure

| Object | Endpoint Slug | SIS Object | Delete Behavior |
| :--- | :--- | :--- | :--- |
| [Subject](./snapshot-subject.md) | `subject` | Subject | Disable |
| [Program](./snapshot-program.md) | `program` | Program | Disable |
| [Program to Subject Association](./snapshot-program-to-subject-association.md) | `programtosubjectassociation` | Program to Subject Association | Disable |
| [Subject to Course Association](./snapshot-subject-to-course-association.md) | `subjecttocourseassociation` | Subject to Course Association | Disable |
| [Subject to Organization Association](./snapshot-subject-to-organization-association.md) | `subjecttoorgassociation` | Subject to Organization Association | Disable |
| [Course Standard Association](./snapshot-course-standard-association.md) | `standardsassociation` | Goal / Standard Association | Purge |

### Institutional Hierarchy

| Object | Endpoint Slug | SIS Object | Delete Behavior |
| :--- | :--- | :--- | :--- |
| [Hierarchy Node](./snapshot-hierarchy-node.md) | `node` | Hierarchy Node | Purge |
| [Hierarchy User Association](./snapshot-hierarchy-user-association.md) | `userassociation` | User Association | Purge |
| [Hierarchy Course Association](./snapshot-hierarchy-course-association.md) | `courseassociation` / `organizationassociation` | Course / Org Association | Purge |

---

## Complete Endpoint Reference

All endpoints follow the base URL pattern:

```text
https://{learn-host}/webapps/bb-data-integration-flatfile-{building-block-id}/endpoint/{object}/{operation}
```

| Object | Store | Refresh | Refresh by DSK | Delete |
| :--- | :--- | :--- | :--- | :--- |
| User | `person/store` | `person/refresh` | `person/refreshlegacy` | `person/delete` |
| Course | `course/store` | `course/refresh` | `course/refreshlegacy` | `course/delete` |
| Organization | `organization/store` | `organization/refresh` | `organization/refreshlegacy` | `organization/delete` |
| Course Membership | `membership/store` | `membership/refresh` | `membership/refreshlegacy` | `membership/delete` |
| Organization Membership | `organizationmembership/store` | `organizationmembership/refresh` | `organizationmembership/refreshlegacy` | `organizationmembership/delete` |
| Term | `term/store` | `term/refresh` | `term/refreshlegacy` | `term/delete` |
| Secondary Institution Role | `secondaryinstrole/store` | `secondaryinstrole/refresh` | `secondaryinstrole/refreshlegacy` | `secondaryinstrole/delete` |
| Observer Association | `associateobserver/store` | `associateobserver/refresh` | `associateobserver/refreshlegacy` | `associateobserver/delete` |
| Course Category | `coursecategory/store` | `coursecategory/refresh` | `coursecategory/refreshlegacy` | `coursecategory/delete` |
| Organization Category | `organizationcategory/store` | `organizationcategory/refresh` | `organizationcategory/refreshlegacy` | `organizationcategory/delete` |
| Course Category Membership | `coursecategorymembership/store` | `coursecategorymembership/refresh` | `coursecategorymembership/refreshlegacy` | `coursecategorymembership/delete` |
| Organization Category Membership | `organizationcategorymembership/store` | `organizationcategorymembership/refresh` | `organizationcategorymembership/refreshlegacy` | `organizationcategorymembership/delete` |
| Subject | `subject/store` | `subject/refresh` | `subject/refreshlegacy` | `subject/delete` |
| Program | `program/store` | `program/refresh` | `program/refreshlegacy` | `program/delete` |
| Program to Subject Association | `programtosubjectassociation/store` | `programtosubjectassociation/refresh` | `programtosubjectassociation/refreshlegacy` | `programtosubjectassociation/delete` |
| Subject to Course Association | `subjecttocourseassociation/store` | `subjecttocourseassociation/refresh` | `subjecttocourseassociation/refreshlegacy` | `subjecttocourseassociation/delete` |
| Subject to Organization Association | `subjecttoorgassociation/store` | `subjecttoorgassociation/refresh` | `subjecttoorgassociation/refreshlegacy` | `subjecttoorgassociation/delete` |
| Course Standard Association | `standardsassociation/store` | `standardsassociation/refresh` | `standardsassociation/refreshlegacy` | `standardsassociation/delete` |
| Hierarchy Node | `node/store` | `node/refresh` | `node/refreshlegacy` | `node/delete` |
| Hierarchy User Association | `userassociation/store` | `userassociation/refresh` | `userassociation/refreshlegacy` | `userassociation/delete` |
| Hierarchy Course Association | `courseassociation/store` | `courseassociation/refresh` | `courseassociation/refreshlegacy` | `courseassociation/delete` |
| Hierarchy Organization Association | `organizationassociation/store` | `organizationassociation/refresh` | `organizationassociation/refreshlegacy` | `organizationassociation/delete` |
| Data Set Status | `dataSetStatus/{dataSetUid}` | — | — | — |

---

## Data Set Status

The `dataSetStatus` endpoint is an operational polling endpoint — not a data feed object — used to check the processing status of a previously submitted data set.

```text
GET .../endpoint/dataSetStatus/{dataSetUid}
```

---

## Notes

- **Courses and Organizations** share the same field structure but use different header names for key identifying fields and are submitted to separate endpoints.
- **Programs** are persisted in Blackboard as courses with a Program service level. The `/program/` endpoint sets this automatically.
- **Subjects** use a double-underscore naming convention in `subject_id` (e.g. `CHEM__abc123`). Keep this in mind when constructing association batch UIDs that reference a Subject — use a different separator to avoid ambiguity.
- **Association batch UIDs** (`external_association_key`) should be constructed by concatenating the two parent batch UIDs unless your source system provides a natural unique key for the relationship.
- **Purge vs Disable** — objects with Purge delete behavior are permanently removed and cannot be recovered. Use Complete Refresh with caution on these objects.
