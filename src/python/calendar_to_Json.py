
#==================================================================
# PURPOSE: Take UVic food service calendar data and exports it in JSON
# 

import json
import io
from file_writer_handler import send_job, execute_jobs


def convert_to_Json(list_of_schedules):
	print 'Formating Output'
	print 'Writing to file'

	with open('../../output/Food_Services_Schedule.txt', 'a') as file_path:
		for item in list_of_schedules:
			url= item.url
			name = item.name
			daysWithHours = item.json_export_hours()
			data = {'Name' : name, 'Url' : url, 'Days': daysWithHours}
			json.dump(data, file_path)
	return 

