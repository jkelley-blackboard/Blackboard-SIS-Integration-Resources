# Blackboard SIS Custom Field Mapping Reference

This document provides **not entirely tested** examples of how to access data fields in Blackboard SIS custom mapping scripts using the Java Map syntax.

---

## 1. Person

| Blackboard Field                      | Java Map Syntax                                             |
|----------------------------------------|-------------------------------------------------------------|
| External Person Key / Batch UID        | `data.getPerson().getSourcedGUID().getSourcedId()`          |
| Username / User ID                     | `data.getPerson().getUserName()`                            |
| First Name                             | `data.getPerson().getName().getGivenName()`                 |
| Last Name                              | `data.getPerson().getName().getFamilyName()`               |
| Email Address                          | `data.getPerson().getEmail()`                              |
| Institution Role                        | `data.getPerson().getRoles().getPrimaryInstitutionRole().getValue()` |
| Secondary Institution Roles             | `data.getPerson().getRoles().getSecondaryInstitutionRoles()` **(TBD)** |
| Extensions (pronouns, etc.)             | `data.getPerson().getExtensions().get('fieldName')` **(TBD)** |

---

## 2. Course Section

| Blackboard Field                               | Java Map Syntax                                                  |
|------------------------------------------------|------------------------------------------------------------------|
| External Course Key / Course Section SourcedId | `data.getCourseSection().getSourcedGUID().getSourcedId()`        |
| Course Section Title / Name                     | `data.getCourseSection().getTitle()`                             |
| Description / Catalog Description             | `data.getCourseSection().getCatalogDescription().getLongDescription()` **or** `.getShortDescription()` if available |
| Data Source                                     | `data.getCourseSection().getDataSource()`                        |
| Start Date                                      | `data.getCourseSection().getStartDate()`                         |
| End Date                                        | `data.getCourseSection().getEndDate()`                           |
| Term / Academic Session                         | `data.getCourseSection().getAcademicSession()` **(TBD)**          |
| Available Flag / Is Available                   | `data.getCourseSection().getIsAvailable()` **(TBD)**              |

---

## 3. Course Membership

| Blackboard Field                        | Java Map Syntax                                                         |
|-----------------------------------------|-------------------------------------------------------------------------|
| External Course Key / Course Section Id | `data.getMembership().getCourseSection().getSourcedGUID().getSourcedId()` **(or similar)** |
| External Person Key / User Id           | `data.getMembership().getPerson().getSourcedGUID().getSourcedId()`      |
| Role in Course (Student / Instructor)   | `data.getMembership().getRole()`                                        |
| Enrollment Date                          | `data.getMembership().getEnrollmentDate()`                              |
| Availability / Is Available             | `data.getMembership().getIsAvailable()` **(TBD)**                       |
| Data Source                              | `data.getMembership().getDataSource()`                                 |

---

## 4. Term (Group Record)

| Blackboard Field                        | Java Map Syntax                                          |
| --------------------------------------- | -------------------------------------------------------- |
| **Term Name** (`<shortDescription>`)    | `data.getGroup().getDescription().getShortDescription()` |
| Term Start Date (`<timeframe><begin>`)  | `data.getGroup().getTimeframe().getBegin()`              |
| Term End Date (`<timeframe><end>`)      | `data.getGroup().getTimeframe().getEnd()`                |
| Sourced ID (`<sourcedGUID><sourcedId>`) | `data.getSourcedGUID().getSourcedId()`                   |
| Data Source                             | `data.getGroup().getDataSource()`                        |
