from monthBuilding import makeCalendarList
startTimes = ['8AM', '9AM', '10AM', '11AM', '12PM', '1PM', '2PM', '3PM', '4PM', '5PM']
endTimes = ['8AM', '9AM', '10AM', '11AM', '12PM', '1PM', '2PM', '3PM', '4PM', '5PM', '6PM', '7PM', '8PM', '9PM', '10PM']
roles = ['M', 'MA', 'C', 'R']

days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

def makeWeekTemplateFromScratchPhaseOne():
    #TODO Modify the form in this html to post to a page with the next phase
    htmlTable = """<form action='/weekOfShifts' id='week' method='post'>
    <table width='100%' border='1px'> 
    <tr> 
    <th> Sunday </th> 
    <th> Monday </th> 
    <th> Tuesday </th> 
    <th> Wednesday </th> 
    <th> Thursday </th> 
    <th> Friday </th> 
    <th> Saturday </th> 
    </tr><tr>"""

    for i in range(7):
        htmlTable = htmlTable + "<td><label> Add Shifts </label><input form='week' type='number' name='{0}'></td>".format(i)

    htmlTable = htmlTable + "</tr></table><label>Build a Weekly Template</label><input type='submit' form='week' name='submitWeek'></form>"

    return htmlTable

def modifyWeekOfShifts(listOfShifts):
    htmlTable = """
    <form name='weekShifts' action='/makeWholeMonth' method='post'>
    <table width='100%' border='1px'>
    <tr>
    <th> Sunday </th> 
    <th> Monday </th> 
    <th> Tuesday </th> 
    <th> Wednesday </th> 
    <th> Thursday </th> 
    <th> Friday </th> 
    <th> Saturday </th> 
    </tr><tr>
    """

    for j in range(len(listOfShifts)): #listOfShifts will be some [6,8,8,8,8,8,9]
        humShifts = listOfShifts[j]
        day = days[j]
        htmlTable = htmlTable + "<td><table><tr><th>Role</th><th>Beg.</th><th>End</th><tr>"
        for i in range(numShifts): #Generates a blank shift for each shift in each day
            htmlTable = htmlTable + "<select name='{0}' form='weekShifts'>".format(day + "RoleNum" + str(i))
            for role in roles:
                htmlTable = htmlTable + "<option value='{0}'>{0}</option>".format(role)
            htmlTable = htmlTable + "</select><select name={0} form='weekShifts'>".format(day + "StartNum" + str(i))
            for i in range(len(startTimes)):
                htmlTable = htmlTable + "<option value='{0}'>{1}</option>".format(str(i + 8), startTimes[i])
            htmlTable = htmlTable + "</select><select name='{0}' form='weekShifts'>".format(day + "EndNum" + str(i))
            for i in range(len(endTimes)):
                htmlTable = htmlTable + "<option value='{0}'>{1}</option>".format(str(i + 8), endTimes[i])
            htmlTable = htmlTable + "</select></table></td>"
        htmlTable = htmlTable + "</tr></table></form>"

    return htmlTable

def makeWholeMonth(template):
    workingIndex = 0
    for dayShifts in template: #template will be some [(Sunday Shifts), (Monday Shifts), (Tuesday Shifts), etc]
        for shift in dayShifts: #dayShifts will be [(Role1, In1, Out1), (Role2, In2, Out2), etc]
            continue