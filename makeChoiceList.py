#This function takes a list of choices or times and returns an HTML option list for use in a select input
#


def makeChoiceList(listIn, listType, choice):
    selectList = ""
    if listType in ['startTime', 'endTime']:
        start = 8
        for time in listIn:
            if start == choice:
                selectList += "<option value='{0}' selected='selected'>{1}</option>".format(str(start), time)
            else:
                selectList += "<option value='{0}'>{1}</option>".format(str(start), time)
            start += 1
    else:
        for req in listIn:
            if req == choice:
                selectList += "<option value='{0}' selected='selected'>{0}</option>".format(choice)
            else:
                selectList += "<option value='{0}'>{0}</option>".format(req)
    return selectList

if __name__ == "__main__":
    pass