Note - this content is availble IN Blackboard on each deployment.
/webapps/dataIntegration/docs/custom_script_examples.html

***

# Custom Field Mapping Script Examples

This document provides examples of **Field Mapping transformations** available through the **Advanced Configuration → “Use a Custom Script”** option.

***

## Introduction

Custom field mapping scripts are written in **JavaScript**.

If you are new to the language, see the  
JavaScript Guide on Mozilla Developer Network.

If a script contains multiple statements, the **value returned** to the Field Mapping infrastructure is the value of the **last statement**.

### Example

```javascript
var h = "Hello";
var w = "World";
h + w;
```

You may also wrap your script in an **anonymous function**, which allows returning values from multiple locations.

```javascript
(function () {
  if (Math.random() > 0.5) {
    return "Heads";
  } else {
    return "Tails";
  }
})();
```

***

## Available Global Variables

In addition to standard JavaScript functionality, the following global variables are available to each mapping script:

### `data`

*   Represents the incoming SIS data object
*   Object type varies by SIS Integration and data type
*   JavaDocs are provided for each SIS Integration Type
*   Example for a **Person** mapping may include name, address, phone, username, password, etc.

### `helper`

*   Provides helper methods for common tasks
*   Some methods are integration‑specific

***

## ScriptHelper API

The `helper` object exposes the following methods:

*   `String getBatchUid(String id)`  
    Generates an identifier prefixed with the SIS-specific Batch UID prefix

*   `String getXPathString(String xmlString, String xPathQuery)`  
    Executes an XPath query on an XML string  
    (see XPath specification)

*   `Object getHelper(String helperName)`  
    Returns an integration‑specific helper object

*   `Object skipAttribute()`  
    Skips the mapped field without changing it

*   `Object skipAttributeIfNull(Object value)`  
    Skips the field only if the value is null

*   `Object skipRecord()`  
    Skips the entire record

*   `Object skipRecordIfNull(Object value)`  
    Skips the record if the value is null

*   Logging helpers:
    *   `logError(String msg)`
    *   `logWarning(String msg)`
    *   `logInfo(String msg)`
    *   `logDebug(String msg)`

***

## Script Examples

These examples assume a theoretical **Person** object passed as `data` with the following structure:

### `Person`

```text
String getUniqueId()
Name getName()
UserInfo getUserInfo()
Map<String, PhoneNumber> getPhoneNumbers()
String getDescription()
String getXmlExtension()
```

### `Name`

```text
String getGiven()
String getFamily()
String getMiddle()
```

### `UserInfo`

```text
String getUsername()
String getPassword()
String getSystemRole()
```

### `PhoneNumber`

```text
String getType()
String getNumber()
```

***

## Simple Value Retrieval

### Get the person’s first name

```javascript
// Equivalent to: data.getName().getGiven();
data.name.given;
```

### Get the person’s home phone number

```javascript
data.phoneNumbers.get('home').number;
```

***

## String Manipulation

### Full name

```javascript
data.name.given + ' ' + data.name.middle + ' ' + data.name.family;
```

### Last name, comma, first initial

```javascript
data.name.family + ', ' + data.name.given.substring(0, 1) + '.';
```

### Lowercase username

```javascript
data.userInfo.username.toLowerCase();
```

### Prefix username

```javascript
'PREFIX_' + data.userInfo.username;
```

### Truncate description to 50 characters

```javascript
(function () {
  var desc = data.description;
  return desc.length > 50 ? desc.substring(0, 50) : desc;
})();
```

***

## Value Normalization

### Convert SIS system role to Learn role

```javascript
(function () {
  var role = data.systemRole;

  if (role === 'SysAdmin') return 'SYSTEM_ADMIN';
  if (role === 'SysSupport') return 'SYSTEM_SUPPORT';
  if (role === 'User') return 'USER';

  return 'USER';
})();
```

***

## Handling Missing or Redundant Data

### Default password

```javascript
(function () {
  return data.userInfo.password || 'pAssw0rD!';
})();
```

### Home phone or work phone fallback

```javascript
(function () {
  var phones = data.phoneNumbers;

  if (phones.containsKey('home')) {
    return phones.get('home').number;
  } else if (phones.containsKey('work')) {
    return phones.get('work').number;
  } else {
    return null;
  }
})();
```

### First available phone number

```javascript
(function () {
  if (!data.phoneNumbers.isEmpty()) {
    return data.phoneNumbers.values().iterator().next().number;
  }
  return null;
})();
```

***

## Using the ScriptHelper

Assume an additional **Person helper** is available with methods:

```text
boolean isStudent(Person p)
boolean isAdministrator(Person p)
```

### Generate Batch UID

```javascript
helper.getBatchUid(data.uniqueId);
```

### Conditional values based on role

```javascript
(function () {
  var personHelper = helper.getHelper('Person');

  if (personHelper.isStudent(data)) {
    return 'I am a Student.';
  } else if (personHelper.isAdministrator(data)) {
    return 'I am an Administrator.';
  } else {
    return 'I am something completely different.';
  }
})();
```

### Extract value from XML using XPath

```javascript
helper.getXPathString(
  data.xmlExtension,
  '/extension/customPassword[1]'
);
```

### Skip attribute if null

```javascript
if (data.name == null) {
  helper.skipAttribute();
} else {
  data.name;
}
```

***

© 2011 Blackboard Inc. Proprietary and Confidential.
