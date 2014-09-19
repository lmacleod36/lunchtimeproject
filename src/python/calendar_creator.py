
#==================================================================
# PURPOSE: gets food service hour of operation data from UVic websites and 
# exports it to either XML or JSON


from calendar import Calendar
from calendar_to_XML import write_to_Xml
from calendar_to_Json import convert_to_Json
from datetime import date
from dateutil import parser
from BeautifulSoup import BeautifulSoup
import Queue
import re 
from soup_handler import find_data_in_soup, make_soup
import urllib2


# Get Dates
# Purpose: Go through webpage and extract dates
# Use these to create calendar with start and end dates
def get_days_hours(Location_URL):
    soup = make_soup(Location_URL)
    calendarDates = Queue.Queue()

    #Use soup to find data on page
    page_data = find_data_in_soup(soup, None, None)
    tables = find_data_in_soup(soup,'table', 'zebra')
    tableHours = find_data_in_soup(soup, 'td', None)

    return tableHours, soup

# get calendars
# Purpose: Passes in urls for locations, creates calendars for each location
# writes schedules to xml and json files
def get_calendars(placesDictionary):
    print 'Starting'
    list_of_schedules = []

    #get data from URL
    for key, value in placesDictionary.iteritems():
        table_days_hours, soup = get_days_hours(value)
        cleaned_days_hours = find_hours(table_days_hours)

        #create calendar
        tempCalendar = create_calendar(key,value)

        #add data
        assign_times_to_calendar(tempCalendar, cleaned_days_hours, list_of_schedules)
    
    #XML Calls
    #write_to_Xml(list_of_schedules)

    #JSON Calls
    convert_to_Json(list_of_schedules)
    return True

# Create calendar
# Purpose:  Creates a calendar Object
def create_calendar(placeName, url):
    aCalendar = Calendar(placeName, url)
    return aCalendar 

# Assign Times to Schedule
# Purpose: Take in a schedule and list of hours, and assign listed hours to appropriate
# day of the week in the schedule
def assign_times_to_calendar(aCalendar,day_hour_List, list_of_schedules):
    day = None
    tempStartTime = None
    tempEndTime = None
    aQueue = Queue.Queue()

    for item in day_hour_List:
        # If item is a date: start gathering info for new day of the week
        if item in aCalendar.hours:
            day = item
            tempStartTime = None
            tempEndTime = None             

        # If item is not a date it must be a time therefore append it to schedule hours
        # Can be in the format "Closed" or an actual time value
        elif item == 'CLOSED':
            value = aCalendar.addHours(day, item)

        else:
            # Assign tempStartTime then tempEndTime
            # If tempStartTime has already been assigned we know the next value is the
            # end time. Assign these values to the passed in schedule 
            if tempStartTime:
                tempEndTime = item
                value = aCalendar.addHours(day, tempStartTime, tempEndTime)

            else:
                tempStartTime = item

    list_of_schedules.append(aCalendar)
    return


# Find Hours
# Purpose: For each table, get the hours for each day that the location is open
# Removes alot of noise and tags that we don't need
# Returned list is in the format [day,startTime,endTime...] or [day,CLOSED...]
# Weeks start on Mondays
def find_hours(table):
    result = []
    for row in table:
        # Strip out HTML tags and unneeded words
        # To Do: Make this a more condensed Regex

        # We don't care about words  (just hours), so strip those annoying letters 
        aString = re.sub('<[a-zA-Z]+>', ' ', str(row))
        aString = re.sub('<[//a-zA-Z]+>', ' ', aString)
        aString = re.sub('((Day)|(Hours))', '', aString)
        aString = re.sub('to', ' ', aString)
        aList = aString.split()
        result.extend(aList)

    # UVic added '&#32;&#32;' aka two spaces to the closing times,  
    # The following removes that from our results 
    for item in result:
        # use 'm' not 'pm' because some times contain '12:00 am'
        # check if at least one 'm' is found
        if item.find('m') > 0:
            tempList = item.split('m')
            newValue = tempList[0]+'m'
            result[result.index(item)] = newValue
    return result



# UPDATE Sept 2014: UVic has removed start and end dates from their calendars (eg: Saturday, 
# Apr 26, 2014 and Wednesday, Aug 20, 2014')
# The following is no longer needed:
# ===============================
# # Convert String to Date
# # Purpose: Take a String in the format "Month Date, Year" and convert to numeric list format
# def convert_string_to_date(aString):
#     months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
#     aDate = aString.replace(',','').split()

#     # Convert month in string format (Apr) to numeric equivalent (04)
#     if aDate[0] in months:
#         index = months.index(aDate[0])
#         aDate[0] = index +1

#     # Convert all values to ints
#     aDate = [int(y) for y in aDate]
#     convertedDate = date(aDate[2], aDate[0], aDate[1])
    
#     return convertedDate


# # Find Tables
# # Purpose: Finds all table elements in the page and returns them as a list
# def find_tables(soup):
#     tempList = []
#     for s in soup.findAll('table' ,attrs={'class': 'zebra'}):
#         tempList.append(s)   
#     return tempList


# # get_Tables
# # Purpose: Find Tables on page (certain tables hold hours of operation)
# def get_tables(soup, list_of_schedules, schedules_on_this_page):
#     #Get all the tables containing hours of opperation on current webpage
#     tableList = find_tables(soup)

#     for aTable in tableList:
#         anItem = tableList.index(aTable)
#         assign_times_to_calendar(schedules_on_this_page[tableList.index(aTable)],(find_hours(aTable)), list_of_schedules)


# # Get Lines With Hours
# # Purpose: Go through list of lines that contained an H4 tag,
# # Find and return ones with hours of opperation in them
# def get_lines_with_hours(aSoupyList):
#     newList = []
#     # String we are looking for:
#     textline = 'Hours of operation'
    
#     for item in aSoupyList:
#         print 'get_lines_with_hours', item
#         if  textline in str(item):
#             newList.append(item)
#     return newList


# # Get Dates from Soup Text
# # Purpose: Use Regex to find text in the format "Month Date, Year"
# # Returns a list of date items
# def get_months(soupText):
#     tempList = []
    
#     # detect date and year using an ugly regex:
#     # Compare month, then check for up to 2 digits indicating date
#     # then exactly two digits for year
#     p = re.compile('((Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s[0-9]{,2}, 20[0-9]{2})')
    
#     # should return two dates
#     result = p.findall(str(soupText))
    
#     for item in result:
#         # To Do: Regex results includes a stray month string
#         #       Remove this string (by reworking Regex)
#         # For now take first item in list ('Month day, year')
#         aDate = convert_string_to_date(item[0])
#         tempList.append(aDate)
#     return tempList