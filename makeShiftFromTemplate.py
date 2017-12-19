from monthBuilding import makeCalendarList
from makeChoiceList import makeChoiceList
import datetime

startTimes = ['8AM', '9AM', '10AM', '11AM', '12PM', '1PM', '2PM', '3PM', '4PM', '5PM']
endTimes = ['8AM', '9AM', '10AM', '11AM', '12PM', '1PM', '2PM', '3PM', '4PM', '5PM', '6PM', '7PM', '8PM', '9PM', '10PM']
roles = ['M', 'MA', 'A', 'C', 'R']

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
    <form name='weekShifts' action='/makewholemonth' method='post'>
    <table width='100%' border='1px'>
    <tr>
    <th> Sunday <input type='hidden' name='0' value='{0}'></th> 
    <th> Monday <input type='hidden' name='1' value='{1}'></th> 
    <th> Tuesday <input type='hidden' name='2' value='{2}'></th> 
    <th> Wednesday <input type='hidden' name='3' value='{3}'></th> 
    <th> Thursday <input type='hidden' name='4' value='{4}'></th> 
    <th> Friday <input type='hidden' name='5' value='{5}'></th> 
    <th> Saturday <input type='hidden' name='6' value='{6}'></th> 
    </tr><tr>
""".format(listOfShifts[0], listOfShifts[1], listOfShifts[2], listOfShifts[3], listOfShifts[4], listOfShifts[5], listOfShifts[6])
    for j in range(len(listOfShifts)):
        numShifts = listOfShifts[j]
        day = days[j]
        htmlTable = htmlTable + """<td valign='top'>
        <table width='100%' border='1px'>
        <tr>
        <td>Role</td>
        <td>Beg.</td>
        <td>End</td>
        </tr>"""
        for i in range(numShifts):
            htmlTable = htmlTable + "<tr><td><select name='{1}'>{0}</select></td>".format(makeChoiceList(roles, "roles", "MA"),str(day + "role" + str(i)))
            htmlTable = htmlTable + "<td><select name='{1}'>{0}</select></td>".format(makeChoiceList(startTimes, "startTime", "8"),str(day + "start" + str(i)))
            htmlTable = htmlTable + "<td><select name='{1}'>{0}</select></td></tr>".format(makeChoiceList(endTimes, "endTime", "17"),str(day + "end" + str(i)))
        htmlTable = htmlTable + "</table></td>"
    htmlTable = htmlTable + """</tr></table>
    <br>
    <label>Year</label>
    <input name='year' type='number' min='2010' max='2025'>
    <label>Month</label>
    <input name='month' type='number' min='1' max='12'>
    <label>Submit Template and Make a Monthly Schedule</label>
    <input type='submit'>
    </form>"""
    return htmlTable

def makeWholeMonthShifts(template, year, month):
    listForm = makeCalendarList(year, month)
    monthName = datetime.date(1900, month, 1).strftime('%B')
    htmlTable = """
    <h1 align="center">{0} {1} </h1>
    <br>
    
    <table width='100%' border='1px'> 
    <tr> 
    <th> Sunday </th> 
    <th> Monday </th> 
    <th> Tuesday </th> 
    <th> Wednesday </th> 
    <th> Thursday </th> 
    <th> Friday </th> 
    <th> Saturday </th> 
    </tr>""".format(monthName,str(year), str(month))

    for row in listForm:
        htmlTable += "<tr>"
        for i in range(len(row)):
            day = row[i]
            if day == "":
                htmlTable += "<td></td>"
            else:
                dayOfShifts = template[i]
                tableRows = ""
                for j in range(len(dayOfShifts)):
                    tableRows = tableRows + "<tr><td>" + str(template[i][j][0]) + "</td><td></td><td>" +  str(template[i][j][1]) + "</td><td>" + str(template[i][j][2]) + "</td></tr>" 
                htmlTable += """<td valign='top'>
                <day style='float: right'>{0}</day>
                <table border='1px' border-collapse='collapse'><tr><th>Role</th><th>Employee</th><th>Beg</th><th>End</th></tr>{1}</table></td>

                """.format(day,tableRows)
        htmlTable += "</tr>"
    htmlTable += "</table>"
    return htmlTable
