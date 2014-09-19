
#==================================================================
# PURPOSE: 
# 

import ConfigParser
import os.path
from datetime import date
from calendar_creator import get_calendars
import argparse


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
    returnValue = get_calendars(food_locations_dictionary)

    #For Testing Without Internet Connection
    # testDictionary= {'Test Spot':'../test/test_page_biblio.html'}
    # returnValue = get_calendars(testDictionary)

# Main
setup()
