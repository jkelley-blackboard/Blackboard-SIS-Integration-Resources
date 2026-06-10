(function() {
    // Blackboard SIS Mapping Script
    // Purpose: Assign course to primary department node
	// You will also need a script for the Primary Association Batch Uid field.

    var sField = 'Primary Node Batch Uid Script ';  // Logging prefix

    //Get department code
    var dept = data.courseSection.org.id;

    //Error handle
	if (!dept) {
        helper.logWarning(sField + 'Department code not found.');
        return; // Exit if there's no department code
    }
	
    helper.logInfo(sField + 'Department code = ' + dept);

    //Return the department code
    return dept;
})();
