(function() {
    // Assign users to IH node based on primaryInstitutionRole
    // Added Node BatchUI expects a list
    
    var sField = 'Added Node BatchUid Script: ';  // Logging prefix

    var primaryRoleObj = data.getPerson().getRoles().get(0).getPrimaryInstitutionRole().getValue();
    if (primaryRoleObj) {
        var primaryRole = primaryRoleObj + '';  // Convert to string
    } else {
        helper.logWarning(sField + 'Primary Institution Role not found. Skip Record');
        helper.skipRecord();
        return;  // Exit the function if primaryRole is not found
    }

    var parentNodeList = [];

    if (primaryRole == 'Student' || primaryRole == 'S' || primaryRole == 'Learner') {
        helper.logInfo(sField + 'Mapping Node to STUDENT');
        parentNodeList[0] = 'STUDENT';
    } else if (primaryRole == 'Instructor' || primaryRole == 'P' || primaryRole == 'Faculty') {
        helper.logInfo(sField + 'Mapping Node to FACULTY');
        parentNodeList[0] = 'FACULTY';
    } else if (primaryRole == 'Staff') {
        helper.logInfo(sField + 'Mapping Node to STAFF');
        parentNodeList[0] = 'STAFF';
    } else if (primaryRole == 'PROSPECTIVE_STUDENT') {
        helper.logInfo(sField + 'Mapping Node to PROSPECTIVE_STUDENT');
        parentNodeList[0] = 'PROSPECTIVE_STUDENT';
    } else {
        helper.logInfo(sField + 'No NODE map for Primary Institution Role');
    }

    return parentNodeList;

})();


//alternate using Object Mapping

(function() {
    // Assign users to IH node based on primaryInstitutionRole
    // Added Node BatchUI expects a list

    var sField = 'Added Node BatchUid Script: ';  // Logging prefix

    var primaryRoleObj = data.getPerson().getRoles().get(0).getPrimaryInstitutionRole().getValue();
    var primaryRole;
    
    if (primaryRoleObj) {
        primaryRole = primaryRoleObj + '';  // Convert to string
    } else {
        helper.logWarning(sField + 'Primary Institution Role not found. Skip Record');
        helper.skipRecord();
        return;  // Exit the function if primaryRole is not found
    }
    
    // This is a map of Role (key) to Node (value)
    var roleMap = {
        'Student': 'STUDENT',
        'S': 'STUDENT',
        'Learner': 'STUDENT',
        'Instructor': 'FACULTY',
        'P': 'FACULTY',
        'Faculty': 'FACULTY',
        'Staff': 'STAFF',
        'PROSPECTIVE_STUDENT': 'PROSPECTIVE_STUDENT'
    };

    // Create the node list and add the 'value' from the map
    var nodeList = [roleMap[primaryRole]];

    if (nodeList[0]) {
        helper.logInfo(sField + 'Mapping Node to ' + nodeList[0]);
        return nodeList;
    } else {
        helper.logInfo(sField + 'No NODE map for Primary Institution Role');
        return null;
    }
})();

