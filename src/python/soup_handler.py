
#==================================================================
# PURPOSE: functions related to manipulating the soup of webpage information
# 

from BeautifulSoup import BeautifulSoup
import calendar_creator
import urllib2

# Find Data in Soup
# Purpose: Searches the soup for string containing dates for schedule
# Returns a list of date items ('Month day, year')
def find_data_in_soup(soup, tagValue, attrValue):
    aList =[]
    soupData = None
    if tagValue == None:
        soupData = soup.findAll('')
    elif attrValue == None:
        soupData = soup.findAll(tagValue)
    else:
        soup.findAll(tagValue, attrs={'class': attrValue})
    
    return soupData
    
    # UPDATE Sept 2014: UVic has removed start and end dates from their calendars (eg: Saturday, 
    # Apr 26, 2014 and Wednesday, Aug 20, 2014')
    # The following has been depreciated:
    # ===============================
    # # Strip hours out of h4 tags
    # listOfRelevantData = calendar_creator.get_lines_with_hours(linesWithH4Tags)
    # print listOfRelevantData

    # After the above call we now have a list of strings
    # Example string: 'Hours of operation between the dates of Saturday, 
    # Apr 26, 2014 and Wednesday, Aug 20, 2014'
    # for item in listOfRelevantData:
    #     aList.extend(calendar_creator.get_months(item))
    # return aList


# Make Soup
# Purpose: use Beautiful soup to query passed in webpage
def make_soup(aUrl):
    soup = None
    #Testing with internet
    try:
        webpage = urllib2.urlopen(aUrl)
        soup = BeautifulSoup(webpage.read())
    except:
        print "failed to read webpage"
        
    

    #Testing without internet
    # try:
    #     soup = BeautifulSoup(open(aUrl))
    # except:
    #     print "failed to read local webpage" 

    return soup
    
