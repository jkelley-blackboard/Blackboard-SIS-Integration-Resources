# Blackboard SIS Custom Field Mapping — Data Model Reference

This document provides examples of how to access data fields in Blackboard SIS custom field mapping scripts using the Java method syntax available through the `data` global variable.

> These are reference examples. Some fields marked **(TBD)** are not yet confirmed against a live integration. For working script examples, see [`scripting/`](../scripting/).

---

## 1. Person

| Blackboard Field | Script Syntax |
|---|---|
| External Person Key / Batch UID | `data.getPerson().getSourcedGUID().getSourcedId()` |
| Username / User ID | `data.getPerson().getUserName()` |
| First Name | `data.getPerson().getName().getGivenName()` |
| Last Name | `data.getPerson().getName().getFamilyName()` |
| Email Address | `data.getPerson().getEmail()` |
| Primary Institution Role | `data.getPerson().getRoles().get(0).getPrimaryInstitutionRole().getValue()` |
| Secondary Institution Roles | `data.getPerson().getRoles().getSecondaryInstitutionRoles()` **(TBD)** |
| Extensions (institution-specific custom fields) | `data.getPerson().getExtensions().get('fieldName')` **(TBD)** |

**On Extensions:** the only confirmed examples of this mechanism in this repo are `bannerSourcedId`, `bannerUserName`, and `bannerUdcId`, seen in the `<extension>` block of [`lis/xml-samples/LIS_person_uploadable_multi_role.xml`](../xml-samples/LIS_person_uploadable_multi_role.xml). (`pronouns` and `inst_email` are a *different*, Snapshot-only mechanism — see [snapshot-user.md](../../snapshot/specs/snapshot-user.md) — not something confirmed via LIS `getExtensions()`.) The same `getExtensions().get('fieldName')` call should work for any other custom field Ellucian's Banner ILP connector is configured to push — class year, campus, and major are plausible candidates. Whether any of those actually arrive, and under what field name, depends entirely on the ILP-to-LIS mapping configured on Ellucian's side; it isn't guaranteed the way a standard field like `institutionRole` is. Check Ellucian's ILP configuration or a live test payload to confirm what extension field names (if any) your instance is actually sending before relying on one.

---

## 2. Course Section

| Blackboard Field | Script Syntax |
|---|---|
| External Course Key / SourcedId | `data.getCourseSection().getSourcedGUID().getSourcedId()` |
| Course Title / Name | `data.getCourseSection().getTitle()` |
| Long Description | `data.getCourseSection().getCatalogDescription().getLongDescription()` |
| Short Description | `data.getCourseSection().getCatalogDescription().getShortDescription()` |
| Data Source | `data.getCourseSection().getDataSource()` |
| Start Date | `data.getCourseSection().getTimeFrames().get(0).getBegin()` |
| End Date | `data.getCourseSection().getTimeFrames().get(0).getEnd()` |
| Term / Academic Session | `data.getCourseSection().getAcademicSession()` |
| Department Name | `data.courseSection.org.orgUnit` |
| Department ID | `data.courseSection.org.id` |
| Available Flag | `data.getCourseSection().getIsAvailable()` **(TBD)** |

---

## 3. Course Membership

| Blackboard Field | Script Syntax |
|---|---|
| External Course Key | `data.getMembership().getCourseSection().getSourcedGUID().getSourcedId()` **(TBD)** |
| External Person Key | `data.getMembership().getPerson().getSourcedGUID().getSourcedId()` |
| Role (Student / Instructor) | `data.getMembership().getRole()` |
| Enrollment Date | `data.getMembership().getEnrollmentDate()` |
| Availability | `data.getMembership().getIsAvailable()` **(TBD)** |
| Data Source | `data.getMembership().getDataSource()` |

---

## 4. Term (Group Record)

| Blackboard Field | Script Syntax |
|---|---|
| Term Name (`<shortDescription>`) | `data.getGroup().getDescription().getShortDescription()` |
| Start Date (`<timeframe><begin>`) | `data.getGroup().getTimeframe().getBegin()` |
| End Date (`<timeframe><end>`) | `data.getGroup().getTimeframe().getEnd()` |
| Sourced ID | `data.getSourcedGUID().getSourcedId()` |
| Data Source | `data.getGroup().getDataSource()` |
