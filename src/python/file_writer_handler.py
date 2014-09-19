
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



