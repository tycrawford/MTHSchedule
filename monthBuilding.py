from calendar import monthrange
import datetime
from makeChoiceList import makeChoiceList
startTimes = ['8AM', '9AM', '10AM', '11AM', '12PM', '1PM', '2PM', '3PM', '4PM', '5PM']
endTimes = ['8AM', '9AM', '10AM', '11AM', '12PM', '1PM', '2PM', '3PM', '4PM', '5PM', '6PM', '7PM', '8PM', '9PM', '10PM']
choices = ['Work', 'Available', 'OFF']

#These functions are built to make an HTML calendar based on year and month input
#MakeCalendarList takes the year and month in and spits out a List of RowLists for the calendar.
#Each RowList corresponds to the actual row one would find on a calendar
#THe list of RowLists represents the full month as a calendar. This will be returned to whatever function calls it
#makeCalendarHTML takes a year month in and runs makeCalendarList
#With the list, makeCalendarHTML is able to make an HTML calendar.
#Looping through each day, it also uses the makeCHoiceList function as imported above to make the list of choices an employee has. 

#TODO Use this fucntionality to also make an HTML schedule and a list of available shifts. 
#TODO Find away to take in the massive form information and submit it to the database. 

def makeCalendarList(year,month):
    startDay = datetime.date(year, month, 1).isoweekday() #Makes Sunday = 0, Saturday = 6
    lastDay = monthrange(year, month)[1]
    listDays = list(range(1, lastDay + 1))
    workingDay = 1
    newMonth = []
    for i in range(6):
        newRow = []
        for j in range(7):
            if i == 0:
                if j == startDay:
                    newRow.append(workingDay)
                    workingDay += 1
                elif j > startDay:
                    newRow.append(workingDay)
                    workingDay += 1
                else:
                    newRow.append("")
            else:
                if workingDay > lastDay:
                    newRow.append("")
                else:
                    newRow.append(workingDay)
                    workingDay += 1 
        newMonth.append(newRow)
        if lastDay in newRow:
            break
    return newMonth
def makeCalendarHTML(year, month):
    #TODO add a new parameter indicating the type of month generated (Request, ShiftView, ScheduleView)
    #TODO use an if/elif/else to generate different schedules based on requests.
    
    listForm = makeCalendarList(year,month)
    monthName = datetime.date(1900, month, 1).strftime('%B')
    htmlTable = """
    <h1 align="center">{0} {1} </h1>
    <form action='/month' method="post" id="wholeMonth" style="float: right"><input type=submit> 
    <input type="text" name="year" value="{1}">
    <input type="text" name="month" value="{2}">
    </form><br>
    
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
        for day in row:
            if day == "":
                htmlTable += "<td></td>"
            else:
                htmlTable += """<td>
                <day style='float: right'>{0}</day><br><br><br>
                <label>Work/Avail/Off</label><select name="{0}choice" form="wholeMonth">{1}</select><br>
                <label>Start Time</label><select name="{0}startTime" form="wholeMonth">{2}</select><br>
                <label>End Time</label><select name="{0}endTime" form="wholeMonth">{3}</select></td>
                """.format(day, makeChoiceList(choices,"choice", "OFF"), makeChoiceList(startTimes,"startTime",8), makeChoiceList(endTimes, "endTime", 22))
        htmlTable += "</tr>"
    htmlTable += "</table>"
    return htmlTable

if __name__ == "__main__":
    print(makeCalendarList(2017,11))

