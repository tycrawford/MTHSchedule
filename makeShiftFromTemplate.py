from monthBuilding import makeCalendarList

days = ["Sunday"]

def makeWeekTemplateFromScratchPhaseOne():
    #TODO Modify the form in this html to post to a page with the next phase
    htmlTable = """<form><table width='100%' border='1px'> 
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
        htmlTable = htmlTable + "<label> Add Shifts </label><input type='text' value='{0}'>".format(i)

    htmlTable = htmlTable + "</table></form>"

    return htmlTable

def makeWholeMonth(template):
    workingIndex = 0
    for dayShifts in template:
        for shift in dayShifts:
            