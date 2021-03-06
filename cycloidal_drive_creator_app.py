"""
This file contains all the functions needed to run the cycloidal drive creator
app. The output of the app is a '.txt' file that contains equations needed to 
use the "Equation Driven Curve" tool with a "Parametric" equation type in 
SolidWorks. It can also output the equation needed for Fusion360 as well as 
Python. The equations will be populated with the values needed to create your
unique cycloidal drive profile, based on your inputs. The '.txt' will also
include the user's input parameters of their unique cycloidal drive rotor; for 
the full curve.


This code has the following requirements needed to run:
• Python 3.9
• NumpPy
• Matplotlib


The Cycloidal Drive equations this program kicks out was made using the
information provided by Joong-Ho Shin and Soon-Man Kwon's paper "On the lobe
profile design in a cycloid reducer using instant velocity center".
https://www.academia.edu/32875937/On_the_lobe_profile_design_in_a_cycloid_reducer_using_instant_velocity_center


Contributors:
• Sean Alford: https://github.com/seanalford
		- Added support for Fusion360
		- Added support for Python
		- Influenced "Preview" section


Author: Omar Younis

"""

import os
import time

from fractions import Fraction
import numpy as np
import matplotlib.pyplot as plt

from tkinter import *
from tkinter import filedialog
from tkinter import ttk



########################################
#           GUI Functions              #
########################################

def get_output_file():
	"""Gets the output file nam and path from the Entry Box."""
	root.filename = filedialog.asksaveasfilename(
						title="Select File",
						filetypes=(("text files", '*.txt'),)
						)
	output_file_path_entry_box.delete(0, END)
	if root.filename.endswith('.txt'):
		output_file_path_entry_box.insert(0, root.filename)
	else:
		output_file_path_entry_box.insert(0, root.filename + '.txt')


def update_progressbar():
    """Starts the animation for the progress bar."""
    my_progress['value'] += (100/5)
    root.update_idletasks()
    time.sleep(0.25)


def stop_progressbar():
    """Stops the animation for the progress bar."""
    my_progress.stop()


def get_info():
	"""
	Gets all data from the form to use in the main code. Returns tuple to make
	information uneditable.
	"""
	rotor_radius = float(rotor_radius_entry.get())
	roller_radius = float(roller_radius_entry.get())
	eccentricity = float(eccentricity_entry.get())
	num_of_rollers = int(num_rollers_entry.get())
	results_filename = output_file_path_entry_box.get()

	return (rotor_radius, roller_radius, eccentricity, 
		    num_of_rollers, results_filename)


def int_check(input_value, warning_box):
	"""Checks if input is a positive integer."""
	try:
		int_value = int(input_value)
		if int_value > 0:
			warning_box.config(text="")
			return True
		else:
			warning_box.config(text="Please type a positive integer.")
			return False
	except ValueError:
		warning_box.config(text="Please type an integer.")
		return False


def pos_num_check(input_value, warning_box):
	"""Checks if input is a positive number."""
	try:
		pos_num_value = float(input_value)
		if pos_num_value > 0:
			warning_box.config(text="")
			return True
		else:
			warning_box.config(text="Please type a positive number.")
			return False
	except ValueError:
		warning_box.config(text="Please type a number.")
		return False


def entry_checker(entry_boxes):
	"""Checks all of the user inputs before using them."""
	box_status = []
	for i in range(0, 3):
		box_status.append(pos_num_check(entry_boxes[i][0], entry_boxes[i][1]))
	box_status.append(int_check(entry_boxes[3][0], entry_boxes[3][1]))

	return box_status



########################################
#              Functions               #
########################################

def create_equations(user_info):
	"""Takes the user's input parameters and creates the two equation strings
	   needed for the SolidWorks, Fusion360 or Python parametric curve feature."""
	
	R = user_info[0]		# Rotor Radius
	Rr = user_info[1]		# Roller Radius
	E = user_info[2]		# Eccentricity
	N = user_info[3]		# Number of Rollers

	outputformat_value = outputformat.get()

	if outputformat_value == 0:		# SolidWorks
		psi = f"arctan(sin({1-N}*t)/(({Fraction(R/(E*N)).limit_denominator()})-cos({1-N}*t)))"
		x_equation = f"X = ({R}*cos(t))-({Rr}*cos(t+{psi}))-({E}*cos({N}*t))"
		y_equation = f"Y = (-{R}*sin(t))+({Rr}*sin(t+{psi}))+({E}*sin({N}*t))"

	elif outputformat_value == 1:	# Fusion360
		psi = f"atan(sin({1-N}*t)/(({Fraction(R/(E*N)).limit_denominator()})-cos({1-N}*t)))"
		x_equation = f"X = (({R}*cos(t))-({Rr}*cos(t+{psi}))-({E}*cos({N}*t))) * 0.1"
		y_equation = f"Y = ((-{R}*sin(t))+({Rr}*sin(t+{psi}))+({E}*sin({N}*t))) * 0.1"

	else:	# Python
		psi = f"np.arctan(np.sin({1-N}*t)/(({Fraction(R/(E*N)).limit_denominator()})-np.cos({1-N}*t)))"
		x_equation = f"X = ({R}*np.cos(t))-({Rr}*np.cos(t+{psi}))-({E}*np.cos({N}*t))"
		y_equation = f"Y = (-{R}*np.sin(t))+({Rr}*np.sin(t+{psi}))+({E}*np.sin({N}*t))"

	return (x_equation, y_equation)


def create_output_file(user_info, equations):
	"""Creates a '.txt' file with the program's results."""
	with open(user_info[-1], 'w') as f_obj:

		# File Headers
		f_obj.write("Generated by 'cycloidal_drive_creator_app.py'\n\n")
		f_obj.write("GitHub Repository: https://github.com/osyounis/cycloidal_drive_creator\n\n")
		f_obj.write("-"*85)
		f_obj.write("\n")

		# Input Parameters Explanation
		f_obj.write("Description of Parameters:\n\n")
		f_obj.write("R  :  Radius of the Rotor\n")
		f_obj.write("Rr :  Radius of the Roller\n")
		f_obj.write("E  :  Eccentricity - Offset from the Input Shaft to the center of the Rotor\n")
		f_obj.write("N  :  Number of Rollers\n\n")
		f_obj.write("-"*85)
		f_obj.write("\n")

		# Actual Input Values
		f_obj.write("Values Used for the Equations:\n\n")
		f_obj.write(f"R  =  {user_info[0]}\n")
		f_obj.write(f"Rr =  {user_info[1]}\n")
		f_obj.write(f"E  =  {user_info[2]}\n")
		f_obj.write(f"N  =  {user_info[3]}\n\n\n")

		# X and Y Equations depending on platform 
		# selected: SolidWorks, Fusion360 or Python.
		outputformat_value = outputformat.get()

		if outputformat_value == 0:		# SolidWorks
			f_obj.write("The Equations to PASTE in SolidWorks' 'Equation Driven Curve' Feature:\n\n")
		elif outputformat_value == 1:	# Fusion360
			f_obj.write("The Equations to PASTE in Fusion360 'Equation Driven Curve' Feature:\n\n")
		else:		# Python
			f_obj.write("The Equations to PASTE in Python code:\n\n")
	
		f_obj.write(f"{equations[0]}\n")
		f_obj.write(f"{equations[1]}\n\n")
		f_obj.write("-"*85)
		f_obj.write("\n")


def preview_fit():
	"""This function plots the rotor and the rollers to preview the fit."""
	# Getting info and setting up plot
	entry_warning_boxes = [(rotor_radius_entry.get(), rotor_radius_warning),
					           (roller_radius_entry.get(), roller_radius_warning),
					           (eccentricity_entry.get(), eccentricity_warning),
					           (num_rollers_entry.get(), num_rollers_warning)]

	entry_box_statuses = entry_checker(entry_warning_boxes)
	if False in entry_box_statuses:
		return

	user_input_info = get_info()
	R = user_input_info[0]		# Rotor Radius
	Rr = user_input_info[1]		# Roller Radius
	E = user_input_info[2]		# Eccentricity
	N = user_input_info[3]		# Number of Rollers
	
	ax = plt.figure(figsize=(8, 8)).add_subplot()

	# Getting Rotor Equation and Plotting Result
	t = np.linspace(0, 2*np.pi, 1000)	# Number of Points
	psi = np.arctan((np.sin((1-N)*t))/((R/(E*N)) - np.cos((1-N)*t)))
	x = (R*np.cos(t))-(Rr*np.cos(t+psi))-(E*np.cos(N*t)) + E			# E is added to offset the Rotor to test fit with rollers
	y = (-R*np.sin(t))+(Rr*np.sin(t+psi))+(E*np.sin(N*t))

	ax.plot(x, y, label="Rotor")

	# Creating Rotor Radius (the circle which the rollers sit on [position away from the origin]) and Plotting Result
	Rt = np.linspace(0, 2*np.pi, 150)	# Number of Points.
	Rx = R * np.cos(Rt)
	Ry = R * np.sin(Rt)

	ax.plot(Rx, Ry, '--g', label="Roller Position (R)")

	# Creating Roller Equation and Plotting All Rollers on Plot
	theta = np.linspace((np.pi/2), (5/2 * np.pi), (N + 1))		# Dividing 2π by number of roller
	Rrt = np.linspace(0, 2*np.pi, 150)							# Number of Points
	
	for index, radian in enumerate(theta):
		Rrx = Rr * np.cos(Rrt) + (R * np.sin(radian))
		Rry = Rr * np.sin(Rrt) + (R * np.cos(radian))

		if index == 0:
			ax.plot(Rrx, Rry, 'r', label="Roller")
		else:
			ax.plot(Rrx, Rry, 'r')
	
	# Showing the Plot
	ax.set(aspect=1)	# Locks the axes so the curve is show properly
	plt.legend(loc='upper right')
	plt.grid()
	plt.show()


def run_main_code():
	"""This is the main code that runs when the Run button is pressed."""
	
	# Reseting GUI
	# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
	stop_progressbar()
	root.update_idletasks()


	# Checking Inputs
	# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
	status_label.config(text="")
	root.update_idletasks()
	status_label.config(text="Checking Inputs")
	root.update_idletasks()
	time.sleep(0.5)
	
	# List of Entry Boxes and their Warning Labels
	entry_warning_boxes = [(rotor_radius_entry.get(), rotor_radius_warning),
					   (roller_radius_entry.get(), roller_radius_warning),
					   (eccentricity_entry.get(), eccentricity_warning),
					   (num_rollers_entry.get(), num_rollers_warning)]

	entry_box_statuses = entry_checker(entry_warning_boxes)
	if False in entry_box_statuses:
		return
	update_progressbar()


	# Getting Inputs
	# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
	status_label.config(text="")
	root.update_idletasks()
	status_label.config(text="Getting Inputs")
	root.update_idletasks()
	time.sleep(0.5)
	user_input_info = get_info()
	update_progressbar()


	# Create Equations
	# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
	status_label.config(text="")
	root.update_idletasks()
	status_label.config(text="Creating Equations")
	root.update_idletasks()
	time.sleep(0.5)
	user_equations = create_equations(user_input_info)
	update_progressbar()


	# Creating Output File
	# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
	status_label.config(text="")
	root.update_idletasks()
	status_label.config(text="Creating Output File")
	root.update_idletasks()
	time.sleep(0.5)
	create_output_file(user_input_info, user_equations)
	update_progressbar()


	# Finish Run
	# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
	time.sleep(0.5)
	status_label.config(text="")
	root.update_idletasks()
	status_label.config(text="Program Complete!")
	update_progressbar()


########################################
#              GUI Code                #
########################################

# Main Setup for App.
root = Tk()
root.title("Cycloidal Drive Rotor Creator")
root.resizable(width=False, height=False)


#  Section 1 of the App (Rotor Params Inputs)
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
dim_frame = LabelFrame(root, text="Dimension Information")
dim_frame.grid(sticky="we", row=0, padx=10, pady=10)

# Rotor Radius
rotor_radius_label = Label(dim_frame, text="Rotor Radius: ", justify='right')
rotor_radius_label.grid(sticky='w', row=0, column=0, padx=(10, 0), pady=(10, 0))

rotor_radius_entry = Entry(dim_frame, width=10)
rotor_radius_entry.grid(sticky='w', row=0, column=1, padx=(0, 10), pady=(10, 0))

rotor_radius_warning = Label(dim_frame, text="", justify='right', fg='#D10000')
rotor_radius_warning.grid(sticky='w', row=1, column=1, padx=(0, 10), pady=(0, 10))

# Roller Radius
roller_radius_label = Label(dim_frame, text="Roller Radius: ", justify='right')
roller_radius_label.grid(sticky='w', row=0, column=3, padx=(60, 0), pady=(10, 0))

roller_radius_entry = Entry(dim_frame, width=10)
roller_radius_entry.grid(sticky='w', row=0, column=4, padx=(0, 10), pady=(10, 0))

roller_radius_warning = Label(dim_frame, text="", justify='right', fg='#D10000')
roller_radius_warning.grid(sticky='w', row=1, column=4, padx=(0, 10), pady=(0, 10))

# Eccentricity
eccentricity_label = Label(dim_frame, text="Eccentricity: ", justify='right')
eccentricity_label.grid(sticky='w', row=2, column='0', padx=(10, 0))

eccentricity_entry = Entry(dim_frame, width=10)
eccentricity_entry.grid(sticky='w', row=2, column=1, padx=(0, 10))

eccentricity_warning = Label(dim_frame, text="", justify='right', fg='#D10000')
eccentricity_warning.grid(sticky='w', row=3, column=1, padx=(0, 10), pady=(0, 10))

# Number of Rollers
num_rollers_label = Label(dim_frame, text="Number of Rollers: ", justify='left')
num_rollers_label.grid(sticky='w', row=2, column=3, padx=(60, 0))

num_rollers_entry = Entry(dim_frame, width=10)
num_rollers_entry.grid(sticky='w', row=2, column=4, padx=(0, 10))

num_rollers_warning = Label(dim_frame, text="", justify='right', fg='#D10000')
num_rollers_warning.grid(sticky='w', row=3, column=4, padx=(0, 10), pady=(0, 10))


#  Section 2 of the App (Program Format)
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
output_format = LabelFrame(root, text="Program Format", padx=5, pady=5)
output_format.grid(sticky="we", row=1, padx=10, pady=10)

outputformat = IntVar()

solidWorks = Radiobutton(output_format, text="SolidWorks", variable=outputformat, value=0)
solidWorks.grid(sticky="w", row=0, column=0, padx=10, pady=10)

fusion360 = Radiobutton (output_format, text="Fusion 360", variable=outputformat,value=1)
fusion360.grid(sticky="we", row=0, column=1, padx=10, pady=10)

python = Radiobutton (output_format, text="Python", variable=outputformat, value=2)
python.grid(sticky="e", row=0, column=2, padx=10, pady=10)

outputformat.set(0)


#  Section 3 of the App (Output File Selection)
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
output_frame = LabelFrame(root, text="Select Output File", padx=5, pady=5)
output_frame.grid(sticky="we", row=2, padx=10, pady=10)

output_file_path_entry_box = Entry(output_frame, width=60)
output_file_path_entry_box.grid(row=0, column=0, padx=10)

output_save_button = Button(output_frame, text="Browse", padx=13, command=get_output_file)
output_save_button.grid(row=0, column=1)


#  Section 4 of the App (Run/Progressbar Section)
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
status_frame = LabelFrame(root, padx=5, pady=5)
status_frame.grid(sticky="we", row=3, padx=10, pady=10)

my_progress = ttk.Progressbar(status_frame, orient=HORIZONTAL, length=300,
                              mode='determinate', maximum=100)
my_progress.grid(sticky="w", row=0, column=0, padx=10, pady=10)

status_label = Label(status_frame, text="", justify='right')
status_label.grid(sticky="e", row=0, column=1, padx=10, pady=10)

preview_button = Button(root, text="Preview", padx=30, command=preview_fit)
preview_button.grid(sticky="w", row=4, padx=10, pady=10)

run_button = Button(root, text="Run", padx=30, command=run_main_code)
run_button.grid(sticky="e", row=4, padx=10, pady=10)


#       Runs the app (App's Main Loop)
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
root.mainloop()