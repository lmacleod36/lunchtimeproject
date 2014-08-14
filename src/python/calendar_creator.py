# calendar_creator is free software: you can redistribute it and/or modify
#    it is under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#==================================================================
# PURPOSE: gets food service hour of operation data from UVic websites and 
# exports it to either XML or JSON


from calendar import Calendar
from calendar_to_XML import write_to_Xml
from calendar_to_Json import write_to_Json
from datetime import date
from dateutil import parser
from BeautifulSoup import BeautifulSoup
import Queue
import re 
from soup_handler import find_data_in_soup, make_soup
import urllib2

#what day of the week is it?  0-6 = Sunday-Saturday
day = date.today()


# Get Dates
# Purpose: Go through webpage and extract dates
# Use these to create calendar with start and end dates
def get_dates(value, key):
    soup = make_soup(value)
    calendarDates = Queue.Queue()

    for aDate in find_data_in_soup(soup):
        calendarDates.put(aDate)

    calendars_on_this_page = []
    # While we have pairs of calendar dates
    while not calendarDates.empty() and calendarDates.qsize() %2 ==0:
        aCalendar = create_calendar(
            str(calendarDates.get()), 
            str(calendarDates.get()), 
            key, value)            
        calendars_on_this_page.append(aCalendar)

    return calendars_on_this_page, soup
  

# get calendars
# Purpose: 'Main' method, passes in urls for locations, creates calendars for each location
# writes schedules to xml file
def get_calendars(placesDictionary):
    # all the calendars per food location. Usually there are 2 or 3 calendars per location
    list_of_schedules = []

    for key, value in placesDictionary.iteritems():
        schedules_on_this_page, soup = get_dates(value, key)
        get_tables(soup, list_of_schedules, schedules_on_this_page)
        
    write_to_Xml(list_of_schedules)
    return True


# Create calendar
# Purpose:  Creates a calendar Object
def create_calendar(tempStartDate, tempEndDate, placeName, url):
    aCalendar = Calendar(tempStartDate, tempEndDate, placeName,url)
    return aCalendar 

# Assign Times to Schedule
# Purpose: Take in a schedule and list of hours, and assign listed hours to appropriate
# day of the week in the schedule
def assign_times_to_calendar(aSchedule,dayOfWeekHoursList, list_of_schedules):
    day = None
    tempStartTime = None
    tempEndTime = None
    aQueue = Queue.Queue()

    for item in dayOfWeekHoursList:
        # If item is a date: start gathering info for new day of the week
        if item in aSchedule.hours:
            day = item
            tempStartTime = None
            tempEndTime = None             

        # If item is not a date it must be a time therefore append it to schedule hours
        # Can be in the format "Closed" or an actual time value
        elif item == 'CLOSED':
            value = aSchedule.addHours(day, item)

        else:
            # Assign tempStartTime then tempEndTime
            # If tempStartTime has already been assigned we know the next value is the
            # end time. Assign these values to the passed in schedule 
            if tempStartTime:
                tempEndTime = item
                value = aSchedule.addHours(day, tempStartTime, tempEndTime)

            else:
                tempStartTime = item

    list_of_schedules.append(aSchedule)
    return


# Convert String to Date
# Purpose: Take a String in the format "Month Date, Year" and convert to numeric list format
def convert_string_to_date(aString):
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    aDate = aString.replace(',','').split()

    # Convert month in string format (Apr) to numeric equivalent (04)
    if aDate[0] in months:
        index = months.index(aDate[0])
        aDate[0] = index +1

    # Convert all values to ints
    aDate = [int(y) for y in aDate]
    convertedDate = date(aDate[2], aDate[0], aDate[1])
    
    return convertedDate


# Find Tables
# Purpose: Finds all table elements in the page and returns them as a list
def find_tables(soup):
    tempList = []
    for s in soup.findAll('table' ,attrs={'class': 'zebra'}):
        tempList.append(s)   
    return tempList


# get_Tables
# Purpose: Find Tables on page (certain tables hold hours of opperation)
def get_tables(soup, list_of_schedules, schedules_on_this_page):
    #Get all the tables containing hours of opperation on current webpage
    tableList = find_tables(soup)

    for aTable in tableList:
        assign_times_to_calendar(schedules_on_this_page[tableList.index(aTable)],(find_hours(aTable)), list_of_schedules)


# Find Hours
# Purpose: For each table, get the hours for each day that the location is open
# Removes alot of noise and tags that we don't need
# Returned list is in the format [day,startTime,endTime...] or [day,CLOSED...]
# Weeks start on Mondays
def find_hours(table):
    result = []
    for row in table:
        # Strip out HTML tags and unneeded words
        # To Do: Could probably make this a more condensed Regex

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
            result[result.index(item)] = tempList[0]+'m'
    return result


# Get Lines With Hours
# Purpose: Go through list of lines that contained an H4 tag,
# Find and return ones with hours of opperation in them
def get_lines_with_hours(aSoupyList):
    newList = []
    # String we are looking for:
    textline = 'Hours of operation between the dates of'
    
    for item in aSoupyList:
        if  textline in str(item):
            newList.append(item)
    return newList


# Get Dates from Soup Text
# Purpose: Use Regex to find text in the format "Month Date, Year"
# Returns a list of date items
def get_months(soupText):
    tempList = []
    
    # detect date and year using an ugly regex:
    # Compare month, then check for up to 2 digits indicating date
    # then exactly two digits for year
    p = re.compile('((Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s[0-9]{,2}, 20[0-9]{2})')
    
    # should return two dates
    result = p.findall(str(soupText))
    
    for item in result:
        # To Do: Regex results includes a stray month string
        #       Remove this string (by reworking Regex)
        # For now take first item in list ('Month day, year')
        aDate = convert_string_to_date(item[0])
        tempList.append(aDate)
    return tempList