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
| Extensions (pronouns, etc.) | `data.getPerson().getExtensions().get('fieldName')` **(TBD)** |

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
