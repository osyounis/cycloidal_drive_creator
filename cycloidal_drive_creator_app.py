"""
This file contains all the functions needed to run the cycloidal drive creator
app. The output of the app is a '.txt' file that contains the coordiantes needed
to create a 'curve' feature in SolidWorks for the cycloidal drive rotor.

This code has the following requirements needed to run:
• Python 3.8
• numpy
• pandas

Author: Omar Younis
"""

import os
import numpy as np
import pandas as pd

from tkinter import *
from tkinter import filedialog
from tkinter import ttk


########################################
#              Settings                #
########################################


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
	output_file_path_entry_box.insert(0, root.filename)


def update_progressbar():
    """Starts the animation for the progress bar."""
    my_progress['value'] += (100/3)
    root.update_idletasks()
    time.sleep(0.25)


def stop_progressbar():
    """Stops the animation for the progress bar."""
    my_progress.stop()


def get_info():
	"""Gets all data from the form to use in the main code."""
	rotor_radius = float(rotor_radius_entry.get())
	roller_radius = float(roller_radius_entry.get())
	eccentricity = float(eccentricity_entry.get())
	num_of_rollers = float(num_rollers_entry.get())
	degree_steps = float(steps_entry.get())
	offset = float(offset_entry.get())
	results_filename = output_file_path_entry_box.get() + ".txt"

	return (rotor_radius, roller_radius, eccentricity, num_of_rollers, 
			degree_steps, offset, results_filename)


def int_check(input_value):
	"""Checks if input is a positive integer."""
	try:
		int_value = int(input_value)
		if int_value > 0:
			num_rollers_warning.config(text="")
			return True
		else:
			num_rollers_warning.config(text="Please type a positive integer.")
			return False
	except ValueError:
		num_rollers_warning.config(text="Please type an integer.")
		return False

#############
#	NEED TO FIX WARNING BOXES TO MATCH WITH ENTRY BOXES. CREATE SECOND VARIABLE.
#	IN FUNCTIONS.
#############
def pos_num_check(input_value):
	"""Checks if input is a positive integer."""
	try:
		pos_num_value = float(input_value)
		if pos_num_value > 0:
			num_rollers_warning.config(text="")
			return True
		else:
			num_rollers_warning.config(text="Please type a positive number.")
			return False
	except ValueError:
		num_rollers_warning.config(text="Please type a number.")
		return False


def num_check(input_value):
	"""Checks if input is a positive integer."""
	try:
		num_value = float(input_value)
		num_rollers_warning.config(text="")
		return True

	except ValueError:
		num_rollers_warning.config(text="Please type a number.")
		return False


########################################
#              Functions               #
########################################



########################################
#              GUI Code                #
########################################

# Main Setup for App.
root = Tk()
root.title("Cycloidal Drive Rotor Creator")
root.resizable(width=False, height=False)

# Sets up correct key presses for Entry Boxes.

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


#  Section 2 of the App (Tolerance Params Inputs)
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
tol_frame = LabelFrame(root, text="Tolerance Information")
tol_frame.grid(sticky="we", row=1, padx=10, pady=10)

# Steps
steps_label = Label(tol_frame, text="Steps: ", justify='right')
steps_label.grid(sticky='w', row=0, column=0, padx=(10, 0), pady=(10, 0))

steps_entry = Entry(tol_frame, width=10)
steps_entry.grid(sticky='w', row=0, column=1, pady=(10, 0))

steps_units_label = Label(tol_frame, text=" Degrees", justify='right')
steps_units_label.grid(sticky='w', row=0, column=2, padx=(0, 10), pady=(10, 0))

steps_warning = Label(tol_frame, text="", justify='right', fg='#D10000')
steps_warning.grid(sticky='w', row=1, column=1, padx=(0, 10), pady=(0, 10))

# Offset
offset_label = Label(tol_frame, text="Offset: ", justify='left')
offset_label.grid(sticky='w', row=0, column=4, padx=(50, 0), pady=(10, 0))

offset_entry = Entry(tol_frame, width=10)
offset_entry.grid(sticky='w', row=0, column=5, pady=(10, 0))

offset_warning = Label(tol_frame, text="", justify='left', fg='#D10000')
offset_warning.grid(sticky='w', row=1, column=5, padx=(0, 10), pady=(0, 10))


#  Section 3 of the App (Output File Selection)
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
output_frame = LabelFrame(root, text="Select Output File", padx=5, pady=5)
output_frame.grid(sticky="we", row=2, padx=10, pady=10)

output_file_path_entry_box = Entry(output_frame, width=60)
output_file_path_entry_box.grid(row=0, column=0, padx=10)

output_save_button = Button(output_frame, text="Save", padx=13)
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

run_button = Button(status_frame, text="Run", padx=30)
run_button.grid(sticky="e", row=0, column=2, padx=10, pady=10)


#       Runs the app (App's Main Loop)
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
root.mainloop()