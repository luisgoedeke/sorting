# sorting
Student project for automatic separation of bottle caps.
Given is a camera, a conveyor belt with 4 light sensors and 3 retractable cylinders that are operated with compressed air. 
The goal of the project is that with the help of machine learning and a camera, the caps are recognized and classified. They are subsequently transported by the cylinders into the respective collection box.

## run.py
Contains the main menu for starting the individual methods. This includes the run for sorting the lids as well as other features such as a function test of all components and an adjustment of the parameters of the separation system. A graphical user interface was created for this purpose. 

## sorting.py
Program for classification and separation of the lids. The process sequence is as follows: Starting the separation; starting the conveyor belt; as soon as light barrier 4 triggers (A lid has fallen out of the separation): Stopping the separation; as soon as light barrier 3 triggers (The lid has moved on the conveyor belt into the camera area): Stopping the conveyor; taking a photo; processing the photo; classifying the lid; pushing the cylinder assigned to the class. If the lid cannot be assigned to a class, none of the cylinders will push and the lid will fall into a reject bin at the end of the conveyor.
### Assignment of the classified cover to the matching cylinder: 
The classes of the three lids contain a target position as an attribute. As soon as the lid has been classified, an element of the identified class is added to queue q1. In the area of cylinder 1, the element is then taken from queue Q1 and the stored target position is compared with the position of the cylinder (cylinder 1: position = 1). If the target position corresponds to the actual position, the cylinder is moved out. Otherwise, the element is inserted into the next queue (queue q2), which is then processed at light barrier 2. The process is repeated on the other cylinders.

### Fill level output
Counter variables are implemented in the program, which store how often the respective cylinder has already been extended. This number corresponds to the number of lids in the collection containers of the respective class. By storing the maximum capacity of the containers, a fill level of the containers can be output.