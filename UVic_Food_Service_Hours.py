# UVic_Food_Service_Hours is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
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

import urllib2
import Queue
import re
import datetime
from datetime import date
from dateutil import parser
from BeautifulSoup import BeautifulSoup
from xml.etree.ElementTree import Element, SubElement, tostring

class TermSchedule:
    def __init__(self, startDate, endDate, name, url):
        self.name = name
        self.startDate = startDate
        self.endDate = endDate
        self.url = url
        self.hours = {
            'Sunday':(),
            'Monday':(),
            'Tuesday':(),
            'Wednesday':(),
            'Thursday':(),
            'Friday':(),
            'Saturday':()
        }
    def addHours(self, day, *args):
        if day in self.hours:
            hoursOfOpperation = list(args)
            self.hours[day] = hoursOfOpperation
            return True
        else: 
            return False

# the names and websites of each food menu
places = [
          ('Arts Place','http://www.uvic.ca/services/food/where/artsplace/index.php'),
           ('BiblioCafe','http://www.uvic.ca/services/food/where/bibliocafe/index.php'),
           ('Cadboro Commons',
            'http://www.uvic.ca/services/food/what/cadboromenu/index.php'),
           ('Caps Bistro','http://www.uvic.ca/services/food/where/capsbistro/index.php'),
           ('Court Cafe','http://www.uvic.ca/services/food/where/courtcafe/index.php'),
           ('Macs','http://www.uvic.ca/services/food/where/macs/index.php'),
           ('Mystic Market','http://www.uvic.ca/services/food/where/mysticmarket/index.php'),
           ('Nibbles and Bytes Cafe','http://www.uvic.ca/services/food/where/nibblesbytes/index.php'),
          ('SciCafe','http://www.uvic.ca/services/food/where/scicafe/index.php'),
          ('Village Greens',
            'http://www.uvic.ca/services/food/what/villagegreensmenu/index.php'),
          ('Village Market','http://www.uvic.ca/services/food/where/villagemarket/index.php')]

#what day of the week is it?  Make 0-6 = Sunday-Saturday
day = date.today()




# ---------------------------------------------------------------------
#  
# Create Schedule
# Purpose: 
# For each food location page, create a soup and search it for H4 tags to get schedule start and end dates
# (Example string: Hours of operation between the dates of Saturday, Apr 26, 2014 and Wednesday, Aug 20, 2014)
# Then pass these off to append open / close times to Term Schedule objects
def get_schedules():
    # all the schedules per food location. Usually there are 2 or 3 schedules per location
    list_of_schedules = []
    total_tables = 0

    for place in places:
        schedules_on_this_page = []
        try:
            webpage = urllib2.urlopen(str(place[1]))
        except:
            print "failed to read webpage"

        soup = BeautifulSoup(webpage.read())

        for s in soup.findAll('h4'):
            scheduleDates = Queue.Queue()
            # Example string: Hours of operation between the dates of Saturday, Apr 26, 2014 and Wednesday, Aug 20, 2014
            textline = 'Hours of operation between the dates of'
            # Check text associated with H4 value

            if textline in s.text:
                daysOfOpperation = get_months(s.text)

                for aDate in daysOfOpperation:
                    scheduleDates.put(aDate)

                # When we have two dates: assume they are the start and end dates 
                # of a schedule and create a schedule
                # To Do : Devise better system for checking start and end dates
                while scheduleDates.qsize() %2 == 0 and scheduleDates.qsize() > 0:
                    tempStartDate = scheduleDates.get()
                    tempEndDate = scheduleDates.get()
                    aSchedule = create_schedule(tempStartDate, tempEndDate, place[0], place[1])
                    schedules_on_this_page.append(aSchedule)

        #Get all the tables containing hours of opperation on current food location page
        tableList = find_tables(soup)
        tempList = []

        for aTable in tableList:
            index = tableList.index(aTable)
            assignTimesToSchedule(schedules_on_this_page[index],(find_hours(aTable)), list_of_schedules)

    formatOutput(list_of_schedules)
    
    return



                
# ---------------------------------------------------------------------
#                
# Create Schedule
# Purpose:  Creates a Term Schedule Object
def create_schedule(tempStartDate, tempEndDate, placeName, url):
    aSchedule = TermSchedule(tempStartDate, tempEndDate, placeName,url)
    
    return aSchedule




# ---------------------------------------------------------------------
#  
# Get Dates from Soup Text
# Purpose: Use Regex to find text in the format "Month Date, Year"
# Returns a list of date time items
def get_months(soupText):
    tempList = []
    # detect date and year using an ugly regex
    p = re.compile('(?:((Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s[0-9]+, 20[0-9]+))+')
    # should return two date times
    result = p.findall(soupText)

    for item in result:
        aDate = convert_string_to_date(item[0])
        tempList.append(aDate)

    return tempList




# ---------------------------------------------------------------------
#  
# Find Tables
# Purpose: Finds all table elements in the page and returns them as a list
def find_tables(soup):
    tempList = []
    for s in soup.findAll('table' ,attrs={'class': 'zebra'}):
        tempList.append(s)   

    return tempList




# ---------------------------------------------------------------------
#  
# Find Hours
# Purpose: For each table, get the hours for each day that the location is open
# Removes alot of noise and tags that we don't need
# Returned list is in the format [day,startTime,endTime...] or [day,CLOSED...]
# Weeks start on Mondays
def find_hours(table):
    result = []
    for row in table:
        # Strip out HTML tags and unneeded words
        # Could probably make this a shorter section
        aString = re.sub('<[a-zA-Z]+>', ' ', str(row))
        aString = re.sub('<[//a-zA-Z]+>', ' ', aString)
        aString = re.sub('((Day)|(Hours))', '', aString)
        aString = re.sub('to', ' ', aString)
        aList = aString.split()
        result.extend(aList)

    return result
            



# ---------------------------------------------------------------------
#  
# Convert String to Date
# Purpose: Take a String in the format "Month Date, Year" and convert to numeric list format
def convert_string_to_date(aString):
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    aDate = aString.replace(',','')
    aDate = aDate.split()

    # Convert month in string format (Apr) to numeric equivalent (04)
    if aDate[0] in months:
        index = months.index(aDate[0])
        aDate[0] = index +1

    # Convert all values to ints
    aDate = [int(y) for y in aDate]
    convertedDate = date(aDate[2], aDate[0], aDate[1])
    
    return convertedDate




# ---------------------------------------------------------------------
#  
# Assign Times to Schedule
# Purpose: Take in a schedule and list of hours, and assign listed hours to appropirate
# location in the schedule
def assignTimesToSchedule(aSchedule,dayOfWeekHoursList, list_of_schedules):
    day = None
    tempStartTime = None
    tempEndTime = None

    for item in dayOfWeekHoursList:
        # If item is a date: start gathering info for new day of the week
        if item in aSchedule.hours:
            day = item
            tempStartTime = None
            tempEndTime = None             

        # If itme is not a date it must be a time therefore append it to schedule hours
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




# ---------------------------------------------------------------------
#  
# Format Output
# Purpose: Get data into xml format
def formatOutput(list_of_schedules):

    # Setting Up varriables that will be needed
    outputString = ''
    lastUpdated= date.today()
    url = ''
    scheduleLocation = ''
    startDate = ''
    endDate = ''
    dayName = ''
    startTime = ''
    endTime = ''

    for schedule in list_of_schedules:
        url = schedule.url
        scheduleLocation = schedule.name
        startDate = schedule.startDate
        endDate = schedule.endDate

        # Schedule is the root for our XML
        root = Element('Schedule')
        child0 = SubElement(root, "Last Updated")
        child0.text = str(lastUpdated)
        child1 = SubElement(root, "URL")
        child1.text = url
        child2 = SubElement(root, "Schedule Location")
        child2.text = scheduleLocation
        child3 = SubElement(root, "Start Date")
        child3.text = str(startDate)
        child4 = SubElement(root, "End Date")
        child4.text = str(endDate)
        child5 = SubElement(root,"Days")

        for day in schedule.hours:
            tempChildDayName = SubElement(child5, 'Day Name')
            tempChildDayName.text = day

            if len(schedule.hours[day]) > 1:
                aList = schedule.hours[day]
                tempChildStartTime = SubElement(child5, 'Start Time')
                tempChildStartTime.text = aList[0]
                tempChildEndTime = SubElement(child5, 'End Time')
                tempChildEndTime.text = aList[1]

            else: 
                tempChildStartTime = SubElement(child5, 'Start Time')
                tempChildStartTime.text = 'CLOSED'
                tempChildEndTime = SubElement(child5, 'End Time')
                tempChildEndTime.text = 'CLOSED'

        xmlOutput =  tostring(root)
        printToFile(xmlOutput)

    return



# ---------------------------------------------------------------------
#  
# Print to File
# Purpose: Append the xml string to to file
def printToFile(xmlString):
    file_path = './Food_Services_Schedule.xml'
    fileout = open(file_path, 'a+')
    fileout.write(xmlString + "\n")
    fileout.close()



# ---------------------------------------------------------------------
#  
#    
#Main
get_schedules()

