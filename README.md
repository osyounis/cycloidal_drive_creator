![Project Banner](./assets/cycloidal-drive-creator-banner.jpg)

# Cycloidal Drive Creator App

## Content
- [Quick Summary](#Quick-Summary)
- [Installation](#Installation)
- [Quick Start](#Quick-Start)
- [Resources](#Resources)
---

## Quick Summary
 A Cycloidal Drive is a mechanism used in the engineering world as a speed reducer for an input shaft while reversing its direction. It can do this for high ratios in a small space. They do this using a rotor that has a unique motion.

Several years ago, I wrote a document for a [blog post](https://blogs.solidworks.com/teacher/2014/07/building-a-cycloidal-drive-with-solidworks.html) on the SolidWorks Education Blog explaining how to design your own cycloidal drive rotor. To summarize, the rotor profile is created using a parametric equation. The parametric equation uses four parameters to construct the rotor’s profile: rotor radius, roller radius, eccentricity, and the number of rollers.

This application takes these four parameters and creates a parametric equation for the rotor profile. This equation and then be copied and used in SolidWorks’ “Equation Driven Curve” feature, to create the rotor profile. The parameters and the parametric equation are saved to a `.txt` file. A link to my original blog can be found in the [Resources](#Resources) section.

---

## Installation
[**Python 3.9**](https://www.python.org/) or higher is required to run this application. If this is your first time installing Python, **please make sure to add python to your computer's PATH**. To do this, make sure you check the **"Add Python to PATH"** box on the installation wizard, as shown in the image below.

![Adding Python to PATH on Install](https://raw.githubusercontent.com/osyounis/cycloidal_drive_creator/main/figures/Python_PATH.JPG)

Once you have the correct Python version installed, you can download and run the `.py` file to use the application.

---

## Quick Start
In order to use this application, you will need to know the following parameters for your custom cycloidal drive: rotor radius, roller radius, eccentricity, and the number of rollers. If you are unfamiliar with the term "eccentricity", it is the offset from the center of the input shaft to the center of the rotor. These descriptions will appear in the output file the application creates. Once you have these parameters, you can use the application. 

Launch the application by double clicking the `.py` file.

![Cycloidal Drive Creator App GUI](https://raw.githubusercontent.com/osyounis/cycloidal_drive_creator/working/figures/GUI_interface_3.JPG)

Input your parameters into the correct fields. Click the "Browse" button to select a name and location for your output file; this is where parametric equation for your rotor will be saved. Once you have filled out all the fields press the "Preview" button to see a plot of your rotor (shown below), or press the "Run" button to create your rotor equations. If any information was entered incorrectly or is missing, the application will stop and flag which fields you need to fix before running it again.

![Cycloidal Drive Creator App Preview](https://raw.githubusercontent.com/osyounis/cycloidal_drive_creator/working/figures/Preview_Window.JPG)

Once the application has successfully run, open the output file. There you will find the parametric equation for your cycloidal drive. You can copy and paste the equation directly into SolidWorks' "Equation Driven Curve" feature wizard. If you would like more information on where to find and how to use the "Equation Driven Curve" feature in SolidWorks, please see my [original blog post](https://blogs.solidworks.com/teacher/2014/07/building-a-cycloidal-drive-with-solidworks.html).

One thing to note is when selecting the range for the parametric equation, all values must be in `radians`. Also you will not be able set the range from `0` to `2π`. If you try to do this, SolidWorks will raise and error and not create the rotor profile. There are a few ways around this. The first, and slightly more complex way, is illustrated in my [original blog](https://blogs.solidworks.com/teacher/2014/07/building-a-cycloidal-drive-with-solidworks.html). Although my original way works, there are a few people who have found simpler solutions to this problem.

The YouTube channel [**stepbystep-robotics**](https://www.youtube.com/channel/UC3Z_DCfdbL7I5nZqf8ezejQ) solved this issue by creating half of the rotor profile (setting the range between `0` and `π`) then mirroring it about a center axis. You can follow his method by [clicking here](https://youtu.be/Nk3aaVcvbpA?t=400).

The YouTube channel [**How To Mechatronics**](https://www.youtube.com/channel/UCmkP178NasnhR3TWQyyP4Gw) solved this issue by setting the profile range just under `2π` (setting the range between `0` and `2π - 0.0009`) and then filling in the gap with a spline. You can follow his method by [clicking here](https://youtu.be/OsS9-FzKN6s?t=444).

Once you have created your profile in SolidWorks, you can then extrude it to the desired thickness.

---

## Resources
- ["On the lobe profile design in a cycloid reducer using instant velocity center" by Joong-Ho Shin and Soon-Man Kwon](https://www.academia.edu/32875937/On_the_lobe_profile_design_in_a_cycloid_reducer_using_instant_velocity_center)
- [My Original Blog Post](https://blogs.solidworks.com/teacher/2014/07/building-a-cycloidal-drive-with-solidworks.html)
- [stepbystep-robotics YouTube Channel](https://www.youtube.com/channel/UC3Z_DCfdbL7I5nZqf8ezejQ)
- [stepbystep-robotics' Cycloidal Drive Video](https://youtu.be/Nk3aaVcvbpA)
- [How To Mechatronics YouTube Channel](https://www.youtube.com/channel/UCmkP178NasnhR3TWQyyP4Gw)
- [How To Mechatronics' Cycloidal Drive Video](https://youtu.be/OsS9-FzKN6s)

---
