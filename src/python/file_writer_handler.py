# file_writer_handler is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
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
# File_Writer_Handler uses queuing to manage when information is written to the output
# This file contains the methods used for adding jobs to the queue, and executing them.
#
# It is based off an example from:
# http://themattreid.com/wordpress/2011/01/20/simple-python-a-job-queue-with-threading/


from multiprocessing import Process, Queue

# set variables
queue = Queue()

# Processor
# Purpose: Processes write queries to file
def processor(file_path):
	fileout = open(file_path, 'w')

	while not queue.empty():
		item = queue.get()
		fileout.write(item + '\n')

	fileout.close()


# Send Job
# Purpose: Add string to queue
def send_job(job):
	     queue.put(job)


# Execute Job
# Purpose: Process for writing to file 
def execute_jobs(file_path):
	writer = Process(target=processor(file_path))
	writer.start()
	writer.join()



