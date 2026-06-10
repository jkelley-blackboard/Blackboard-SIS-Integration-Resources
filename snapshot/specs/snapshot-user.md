---
title: "Snapshot Flat File — User"
id: snapshot-flatfile-user
categories: SIS, Snapshot Flat File
published: "2026-04-22"
edited: "2026-04-22"
author: "Jeff Kelley, Principal Solutions Engineer, Blackboard Inc."
---

# User

**SIS Object:** Person  
**Endpoint:** `/endpoint/person/`  
**Insert/Update behavior:** Smart Insert or Update  
**Delete behavior:** Disable (account is disabled, not removed)

The User object provisions and updates user accounts in Blackboard Learn. Each user is identified by a permanent `external_person_key` that must never change for the lifetime of the account. The database cannot merge data between distinct accounts.

---

## Endpoints

| Operation | URL |
| :--- | :--- |
| Store | `.../endpoint/person/store` |
| Complete Refresh | `.../endpoint/person/refresh` |
| Complete Refresh by Data Source | `.../endpoint/person/refreshlegacy` |
| Delete | `.../endpoint/person/delete` |

---

## Fields

| Field | Header | Required | Unique | Format / Values / Max | Comments |
| :--- | :--- | :---: | :---: | :--- | :--- |
| Batch Uid | `external_person_key` | Yes | Yes | Max 64 | Permanent, non-changing identifier. The database cannot merge data between distinct accounts. |
| Data Source Key | `data_source_key` | Yes | No | Max 256, multi-byte | May be supplied by the integration configuration rather than the file. |
| First Name | `firstname` | Yes | No | Max 100, multi-byte |  |
| Last Name | `lastname` | Yes | No | Max 100, multi-byte |  |
| Username | `user_id` | Yes | Yes | Max 50, multi-byte | The username used to log into Blackboard. Must be globally unique. |
| Available | `available_ind` | No | No | `Y` \| `N` | Establishes availability within Blackboard Learn. |
| Birthdate | `birthdate` | No | No | `yyyymmdd` |  |
| City | `city` | No | No | Max 50, multi-byte |  |
| Company | `company` | No | No | Max 100, multi-byte |  |
| Country | `country` | No | No | Max 50, multi-byte |  |
| Department | `department` | No | No | Max 100, multi-byte |  |
| Domain Name | `domain_name` | No | No | Max 255 | Must match a configured hostname. Invalid values silently ignored. Set at insert only — updates are ignored. e.g. `blackboard.college.edu` |
| Education Level | `educ_level` | No | No | See [Education Level Values](#education-level-values) |  |
| Email | `email` | No | No | Max 100 | Blackboard recommends this not be null — users without an email address cannot send email. |
| Gender | `gender` | No | No | `Not Disclosed` \| `Male` \| `Female` |  |
| Home Phone | `h_phone_1` | No | No | Max 50, multi-byte |  |
| Home Phone (Secondary) | `h_phone_2` | No | No | Max 50, multi-byte |  |
| Institution Email | `inst_email` | No | Yes | Max 254 | Can be set to null. No email communications are sent to this address. Used for third-party integrations only. |
| Job Title | `job_title` | No | No | Max 100, multi-byte |  |
| Middle Name | `middlename` | No | No | Max 100, multi-byte |  |
| Mobile Phone | `m_phone` | No | No | Max 50, multi-byte |  |
| Name Pronunciation | `TBC` | No | No | Max 1000, multi-byte | Phonetic spelling or pronunciation guide. Header value pending confirmation. |
| Other Name | `othername` | No | No | Max 100 | Alternate preferred name. |
| Password | `passwd` | No | No | Max 32, multi-byte | If not provided, Learn auto-populates a SHA-512 hash. |
| Password Encryption Type | `pwencryptiontype` | No | No | `MD5` \| `SSHA` |  |
| Primary Institution Role | `institution_role` | No | No | — | Determines the user's view of Portal Modules. See Manage Institution Roles in System Admin for valid values on your system. |
| Pronouns | `pronouns` | No | No | Max 1000 | Multiple values accepted using comma as delimiter. |
| Replacement Batch Uid | `new_external_person_key` | No | Yes | Max 64, multi-byte | Use only when a user's `external_person_key` must change. |
| Replacement Data Source Batch Uid | `new_data_source_key` | No | No | — | UI mapping: `script.flatfile.UserReplacementDataSourceBatchUid` |
| Row Status | `row_status` | No | No | `enabled` \| `disabled` \| `deleted` | `enabled`: normal access. `disabled`: visible but not editable. `deleted`: scheduled for removal. |
| State / Province | `state` | No | No | Max 50, multi-byte |  |
| Street 1 | `street_1` | No | No | Max 100, multi-byte |  |
| Street 2 | `street_2` | No | No | Max 100, multi-byte |  |
| Student ID | `student_id` | No | No | Max 100, multi-byte | Display only — not used for lookup or matching. |
| Suffix | `suffix` | No | No | Max 100, multi-byte |  |
| System Role | `system_role` | No | No | See [System Role Values](#system-role-values) | Defaults to `none` if not provided. |
| Title | `title` | No | No | Max 100, multi-byte |  |
| Website | `webpage` | No | No | Max 100 | URL of the user's personal web page. |
| Work Phone | `b_Phone_1` | No | No | Max 50, multi-byte |  |
| Work Phone (Secondary) | `b_phone_2` | No | No | Max 50, multi-byte |  |
| Zip / Postal Code | `zip_code` | No | No | Max 50, multi-byte |  |

---

## Education Level Values

| Value |
| :--- |
| `K-8` |
| `high school` |
| `freshman` |
| `sophomore` |
| `junior` |
| `senior` |
| `graduate school` |
| `post-graduate school` |

---

## System Role Values

The `system_role` field accepts the following string values. If not provided, defaults to `none`. To assign a custom system role, use the **Role ID** found in **Administrator Panel > System Roles**.

| Role | Accepted Values |
| :--- | :--- |
| User Administrator | `account_admin`, `accountadmin`, `user_admin` |
| System Support | `system_support`, `syssupport` |
| Course Creator | `course_creator`, `creator` |
| Support | `course_support`, `support` |
| Guest | `guest` |
| None | `none` |
| Observer | `observer` |
| Portal Administrator | `portal_admin`, `portal` |
| System Administrator | `sys_admin`, `sysadmin`, `system_admin` |
| eCommerce Administrator | `ecommerce_admin` |
| Card Office Administrator | `card_office_admin` |
| Store Administrator | `store_admin` |

---

## Sample Feed File

Header row is required. Column order is flexible. Values are pipe-delimited.

```text
external_person_key|data_source_key|firstname|lastname|user_id|email|available_ind|institution_role|system_role|row_status
STU-100042|SIS-IMPORT-2025|Maria|Santos|msantos|msantos@university.edu|Y|Student|none|enabled
```

---

## Notes

- **`external_person_key` must never change.** The database cannot merge data between distinct accounts. Use `new_external_person_key` only in the rare case a key genuinely must be replaced.
- **Passwords.** If `passwd` is not supplied, Blackboard auto-populates the field with a SHA-512 hash. Encourage users to set their own password on first login.
- **Email.** Blackboard strongly recommends `email` not be null. Users without an email address cannot send email from within Blackboard.
- **`inst_email`** is a unique identifier used for third-party integrations only. No Blackboard email communications are sent to this address. It cannot be set via the batch file UI (Users > Create).
- **`domain_name`** is set at insert only. Subsequent updates to this field are silently ignored.
- **Data Source Key** may be supplied by the integration configuration. If configured at the integration level it does not need to appear in the file.
