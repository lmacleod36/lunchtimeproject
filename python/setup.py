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
#==================================================================
# PURPOSE: 
# 



import ConfigParser
import os.path
from datetime import date
from UVic_Food_Service_Hours import get_schedules


# Initiate the Config Parser
# Purpose:
# Based on Example from : https://wiki.python.org/moin/ConfigParserExamples
def init_config_parser():
    Config = ConfigParser.ConfigParser()
    Config.read("config.ini")
    return Config

 
# Config Section Map
# Purpose: Get Information from Config Section
# Returns a dictionary
# Taken from Example: https://wiki.python.org/moin/ConfigParserExamples
def get_config_section(section, Config):
    a_Dictionary = {}
    options = Config.options(section)
    for option in options:
        try:
            a_Dictionary[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            a_Dictionary[option] = None
    return a_Dictionary


# Set Last Update
# Purpose: When the script is run, check last time data was updated
# If no file exists create config file with sample dummy data.
def set_last_update(Config):
    # Check if file exists
    if os.path.isfile('config.ini'):
        cfgfile = open('config.ini','w')
        Config.set('LastRunDate','LastUpdate', date.today())
        Config.write(cfgfile)
        cfgfile.close()
    # If file does note exist create it
    else:
        print 'No Config File, Creating Sample Template'
        create_config_file()
    return


# Create Config File
# Purpose: If no config file exists, create one with sample dummy data
def create_config_file(Config):
    cfgfile = open('config.ini','w')
    Config.set('LastRunDate','LastUpdate', date.today())
    Config.set('FoodLocations', 'McDonalds', 'http://www.mcdonalds.com/us/en/home.html')
    Config.write(cfgfile)
    cfgfile.close()
    

# Setup
# Purpose: Create the Config Parser, Get Data from Config File,
def setup():
    Config = init_config_parser()
    food_locations_dictionary = get_config_section('FoodLocations', Config) 
    last_update = get_config_section('LastRunDate', Config)['lastupdate']

    # Compare update date to current date, if different, update data
     if not str(date.today()) == str(last_update):
        print 'Updating Data'
    set_last_update(Config)
    returnValue = get_schedules(food_locations_dictionary)

    #For Testing Without Internet Connection
    # testDictionary= {'Test Spot':'../test/test_page_biblio.html'}
    # returnValue = get_schedules(testDictionary)

# Main
setup()
