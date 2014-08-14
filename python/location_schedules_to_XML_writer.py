# Location Schedules To XML Writer is free software: you can redistribute it and/or modify
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
#PURPOSE


from xml.etree.ElementTree import Element, SubElement, tostring
from file_writer_handler import send_job, execute_jobs


# Format Output
# Purpose: Get data into xml format
def write_schedules_to_Xml(list_of_schedules):
    print 'Formating Output'

    for schedule in list_of_schedules:
        url = schedule.url
        scheduleLocation = schedule.name
        startDate = schedule.startDate
        endDate = schedule.endDate

        # Schedule is the root for our XML
        root = Element('Schedule')

        childURL = SubElement(root, "URL")
        childURL.text = url

        childLocation = SubElement(root, "Schedule Location")
        childLocation.text = scheduleLocation

        childStartDate = SubElement(root, "Start Date")
        childStartDate.text = str(startDate)

        childEndDate = SubElement(root, "End Date")
        childEndDate.text = str(endDate)

        childDays = SubElement(root,"Days")
        
        for day in schedule.hours:
            tempChildDayName = SubElement(childDays, 'Day Name')
            tempChildDayName.text = day

            if len(schedule.hours[day]) > 1:
                aList = schedule.hours[day]
                tempChildStartTime = SubElement(childDays, 'Start Time')
                tempChildStartTime.text = aList[0]
                tempChildEndTime = SubElement(childDays, 'End Time')
                tempChildEndTime.text = aList[1]

            else: 
                tempChildStartTime = SubElement(childDays, 'Start Time')
                tempChildStartTime.text = 'CLOSED'
                tempChildEndTime = SubElement(childDays, 'End Time')
                tempChildEndTime.text = 'CLOSED'

        xmlOutput =  tostring(root)
        send_job(xmlOutput)

    print 'Writing to file'
    execute_jobs()
    return
