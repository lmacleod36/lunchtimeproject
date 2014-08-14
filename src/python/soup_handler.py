# soup_handler is free software: you can redistribute it and/or modify
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
# PURPOSE: functions related to manipulating the soup of webpage information
# 


from BeautifulSoup import BeautifulSoup
import urllib2

# Find Data in Soup
# Purpose: Searches the soup for string containing dates for schedule
# Returns a list of date items ('Month day, year')
def find_data_in_soup(soup):
    aList =[]
    linesWithH4Tags = soup.findAll('h4')

    # Strip hours out of h4 tags
    listOfRelevantData = get_lines_with_hours(linesWithH4Tags)
    
    # After the above call we now have a list of strings
    # Example string: 'Hours of operation between the dates of Saturday, 
    # Apr 26, 2014 and Wednesday, Aug 20, 2014'
    for item in listOfRelevantData:
        aList.extend(get_months(item))

    return aList


# Make Soup
# Purpose: use Beautiful soup to query passed in webpage
def make_soup(aUrl):
    soup = None
    #Testing with internet
    try:
        webpage = urllib2.urlopen(aUrl)
    except:
        print "failed to read webpage"
        
    soup = BeautifulSoup(webpage.read())

    #Testing without internet
    # try:
    #     soup = BeautifulSoup(open(aUrl))
    # except:
    #     print "failed to read local webpage" 

    return soup
    
