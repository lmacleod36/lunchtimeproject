# calendar_to_Json is free software: you can redistribute it and/or modify
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
# PURPOSE: Take UVic food service calendar data and exports it in JSON
# 

import json
from file_writer_handler import send_job, execute_jobs


def write_to_Json(list_of_schedules):
	for item in list_of_schedules:
		print item.name

def convert_to_Json():
	pass