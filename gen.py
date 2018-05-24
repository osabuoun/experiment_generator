from pathlib import Path
from pprint import pprint
import ntpath, os, sys, json, ast

template = {}
template_job = {}
current_dir = os.path.dirname(sys.argv[0])
def read_template():
	global template, template_job, current_dir
	json_file_path =  current_dir + '/template.json'
	json_file = open(json_file_path,'r')
	content = json_file.read()
	template = ast.literal_eval(content)
	template_job = template['jobs'][0]
	#print(template_job)
	json_file.close()

def gen_job(file_name, index):
	job = {}

	task = {}

	task['data'] = []
	template_task = template_job['tasks'][0] 
	for datum in template_task['data']:
		task['data'].append(datum)

	task['data'].append(file_name)	

	task['command'] = template_task['command']

	task['id'] = "{}_{}".format(template_task['id'], index)

	job['tasks'] = [task]

	job['data'] = template_job['data']

	job['command'] = template_job['command']

	job['params'] = template_job['params']

	job['id'] = "{}_{}".format(template_job['id'], index)

	#print(job)
	return job

def process_jobs(URL, jobs):
	global template
	read_template()
	template['jobs'] = []
	path = Path(jobs)
	print("Path: " + str(path))
	if (path.exists()):
		index = 0
		for x in sorted(list(path.glob('*.*'))):
			if not x.is_dir():
				file_name = URL + ntpath.basename(str(x))
				job = gen_job(file_name, index)
				template['jobs'].append(job)
				#print(job)
				index += 1

		with open(sys.argv[1] + "/../experiment.json", 'w') as experiment_file:  
			json.dump(template, experiment_file,indent=4, sort_keys=False)
	else:
		print("Jobs Directory doesn't exist")

process_jobs("http://jobserver.hopto.org/repast/exp_02/input/", sys.argv[1])
pprint(template)
