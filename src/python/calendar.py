# calendar.py is free software: you can redistribute it and/or modify
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
# PURPOSE: methods and variables needed for storing calendar information
# 


# Term Schedule
# Purpose: Class that holds information used to create the xml and json schemas
class Calendar:
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



# Add Hours
# Purpose: Add the hours of operation to a particular day
# Extra args represent hours, can either be 'Closed' or two time values (eg 5:00pm, 6:00pm)        
    def addHours(self, day, *args):
        if day in self.hours:
            hoursOfOpperation = list(args)
            self.hours[day] = hoursOfOpperation
            return True
        else: 
            return False