(function () {
	//This script extends a course's end date 8 or 14 days based on the TERM format.

  //prefix for logging
	sField = "End Date: ";


  //get and test the values for startDate, endDate and termID
    var startDate = data.getCourseSection().getTimeFrames().get(0).getBegin();
	if (startDate === null) {
        helper.logError(sField + "Start date blank, course not created");
        return helper.skipRecord();
    }

    var termID = data.getCourseSection().getAcademicSession();
    if (termID === null) {
        helper.logError(sField + "Missing termID, course not created");
        return helper.skipRecord();
    }

    var endDate = data.getCourseSection().getTimeFrames().get(0).getEnd();
    if (endDate === null) {
        endDate = startDate.clone();
        helper.logWarning(sField + "Missing endDate, set to same as startDate");
    }

  //regular expression checks for four numbers followed by two letters
    var re = /^\d{4}[a-zA-Z]{2}$/;

    if (re.test(termID) && termID.length < 8) {
        if (termID.length === 6) {
          //example 2024SP
          endDate.add(java.util.Calendar.DATE, 14);
          helper.logInfo(sField + "Added 14 days to endDate");
        } else {
            // example 2024CE2
            endDate.add(java.util.Calendar.DATE, 8);
            helper.logInfo(sField + "Added 8 days to endDate");
        }
    } else {
        endDate.add(java.util.Calendar.DATE, 8);
        helper.logWarning(sField + "Invalid termID format. Added 8 days to endDate");
    }

    //true up the hours, min, sec to the end of the day
    endDate.set(java.util.Calendar.HOUR_OF_DAY, 23);
    endDate.set(java.util.Calendar.MINUTE, 59);
    endDate.set(java.util.Calendar.SECOND, 59);
    
    //log the result
    helper.logInfo("Setting the endDate to :" + endDate.toString);
    return endDate;
})();
