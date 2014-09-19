
#==================================================================
# PURPOSE: methods and variables needed for storing and extracting calendar information
# 


# Term Schedule
# Purpose: Class that holds information used to create the xml and json schemas
class Calendar:
    def __init__(self, name, url):
        self.name = name

        # UPDATE Sept 2014: UVic has removed start and end dates from their calendars (eg: Saturday, 
        # Apr 26, 2014 and Wednesday, Aug 20, 2014')
        # The following his no longer needed:
        # ===============================
        # self.startDate = startDate
        # self.endDate = endDate


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


#Export Hours
# Purpose: Return hours and days in a json format
    def json_export_hours(self):
        listOfHours = []

        for key in self.hours:
            times= self.get_hours(key)
            if len(times)<2:
                tempDictionary = { "Day": key, "Start": times[0], "End": times[0]}
            else:
                tempDictionary = { "Day": key, "Start": times[0], "End": times[1]}
            listOfHours.append(tempDictionary)

        return listOfHours

# Get hours
# Purpose: Return hours based on passed in day of week
# Returns a list
    def get_hours(self, dayOfWeek):
        return self.hours.get(dayOfWeek)
        

