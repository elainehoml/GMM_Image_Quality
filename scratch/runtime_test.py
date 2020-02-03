from java.lang import Runtime
from java.io import BufferedReader, InputStreamReader

# Set up parameters for python script to run here
#path = "C:/Users/emlh1n13/OneDrive - University of Southampton/Data/2019-20/GMM_Image_Quality/scratch"
#script = "cmd_test.py"

def run_CPython(path, script):
	"""
	Run CPython script from command prompt

	Parameters
	----------
	path : str
		Path to python script
	script : str
		Name of python script to run

	Returns
	-------
	list
		Output from stdout
	list
		Output from stderr
	"""

	# Command to run
	cmd_str = "cmd /k cd {} & python {} & exit()".format(path, script)

	# Start a new process, run python script from cmd
	run = Runtime.getRuntime()
	proc = run.exec(cmd_str)

	# Collect output from stdout and stderr, print to console
	stdout_reader = BufferedReader(InputStreamReader(proc.getInputStream()))
	stderr_reader = BufferedReader(InputStreamReader(proc.getErrorStream()))

	print("stdout: \n")
	stdout = print_output(stdout_reader)
	
	print("stderr: \n")
	stderr = print_output(stderr_reader)

	return stdout, stderr

def print_output(output_reader):
	"""
	Prints output of stdout or stderr to console

	Parameters
	----------
	output_reader : BufferedReader object
		Reads either stdout or stderr
		
	Returns
	-------
	list
		List of all lines in output_reader as str
	"""
	output_list = []
	output_single = output_reader.readLine()
	while output_single != None: # while line in output_reader is not empty
		output_list.append(output_single) # append this line
		output_single = output_reader.readLine() # advance to next line of output_reader

	# print to console
	for line in output_list:
		print(line)
	print("\n")

	return output_list
#
#run_CPython(path, script)
#print("done")