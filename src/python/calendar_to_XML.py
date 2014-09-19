# calendar_to_XML is free software: you can redistribute it and/or modify
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
#==================================================================
# PURPOSE: Take UVic food service calendar data and exports it in XML.


from xml.etree.ElementTree import Element, SubElement, tostring
from file_writer_handler import send_job, execute_jobs


# Format Output
# Purpose: Get data into xml format
def write_to_Xml(list_of_schedules):
    print 'Formating Output'

    for schedule in list_of_schedules:
        url = schedule.url
        scheduleLocation = schedule.name

        # Schedule is the root for our XML
        root = Element('Schedule')

        childURL = SubElement(root, "URL")
        childURL.text = url

        childLocation = SubElement(root, "Schedule_Location")
        childLocation.text = scheduleLocation

        # UPDATE Sept 2014: UVic has removed start and end dates from their calendars (eg: Saturday, 
        # Apr 26, 2014 and Wednesday, Aug 20, 2014')
        # The following is no longer needed:
        # ===============================
        # childStartDate = SubElement(root, "Start Date")
        # childStartDate.text = str(startDate)

        # childEndDate = SubElement(root, "End Date")
        # childEndDate.text = str(endDate)

        childDays = SubElement(root,"Days")
        
        for day in schedule.hours:
            tempChildDate = SubElement(childDays, 'Date')
            tempChildDayName = SubElement(tempChildDate, 'Day_Name')
            tempChildDayName.text = day

            if len(schedule.hours[day]) > 1:
                aList = schedule.hours[day]
                tempChildStartTime = SubElement(tempChildDate, 'Start_Time')
                tempChildStartTime.text = aList[0]
                tempChildEndTime = SubElement(tempChildDate, 'End_Time')
                tempChildEndTime.text = aList[1]

            else: 
                # tempChildStartTime = SubElement(childDays, 'Start Time')
                # tempChildStartTime.text = 'CLOSED'
                # tempChildEndTime = SubElement(childDays, 'End Time')
                tempChildEndTime.text = 'CLOSED'

        xmlOutput =  tostring(root)
        send_job(xmlOutput)

    print 'Writing to file'
    file_path = '../../output/Food_Services_Schedule.xml'
    execute_jobs(file_path)
    return
