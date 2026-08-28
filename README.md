# Image Annotator

**Download the Current Version (1.1.1)**

**Windows Users**

This is a Python application using the PySide6 GUI API, but you do not need to have either Python nor PySide6 installed on your machine to run this program. The Windows distribution of this program is as a single stand-alone executable file, ImageAnnotator.exe.  The software has been tested on Windows 11.

- Download the **[ImageAnnotator.exe](https://github.com/mathprofdes/Image-Annotator/releases/download/v1.1.1/ImageAnnotator.exe)** file.
- From Windows Explorer double-click the ImageAnnotator.exe file.



**MacOS (Silicon) Users**

This is a Python application, but you do not need to have either Python nor its dependency packages installed on your machine to run this program. The MacOS distribution of this program is a MacOS application for the M series Macs.  The software has been compiled and tested on a Mac M3 running Tahoe.

- Download the **[ImageAnnotator.zip](https://github.com/mathprofdes/Image-Annotator/releases/download/v1.1.1/ImageAnnotator.zip)** file.  Safari should automatically unzip the application.  
  - Note: Alternatively, you can download the **[ImageAnnotator.app.tar.gz](https://github.com/mathprofdes/Image-Annotator/releases/download/v1.1.1/ImageAnnotator.app.tar.gz)** file, and using Finder, extract the application from it.
- In Finder double-click the ImageAnnotator application.  If you get a warning that the file cannot be run you can do the following.
  - Open the System Settings.
  - Click Privacy & Security on the side list.
  - Scroll down to the  security section.
  - Click Open Anyway.
  - Type in your password to confirm.
- You can run the program from any folder on the machine or drag it into your Applications folder and run it from there. 

**Linux Users**

This is a Python application using the PySide6 and several other packages. The easiest way to run this program is either from the source code using PyCharm or to create an executable file for your system. Please see the instructions below.


--- 

**Running the Program in PyCharm**

- Download and extract the Source Code file from the most current release. 
- Create a new PyCharm project named ImageAnnotator, use a virtual environment.
- Copy all the files and directories from the source code directory over to the project in PyCharm.
- From the PyCharm package manager install the PySide6 (6.10.0) package.
- Run the program.

**Create an Executable for Your System**

To create an executable for your system, make the PyCharm project as above. Then, 

- From the PyCharm package manager install pyinstaller.
- In the terminal in PyCharm, run ``pyinstaller -F --windowed ImageAnnotator.py``.  This will create a ImageAnnotator.spec file.
- Open the ImageAnnotator.spec file in PyCharm and change the datas line to ``datas=[('icons','icons'),('Help','Help')],``
- In the terminal in PyCharm, run ``pyinstaller ImageAnnotator.spec``.
- A ``dist`` directory will have been created and in it is a single file ``ImageAnnotator`` that is an executable for your system.
- Copy this executable to where you want to store it and you can run it like any other program on your system. 

---

**Notes:** 

- A png file of a program icon  **[ImageAnnIcon.png](https://github.com/mathprofdes/Image-Annotator/releases/download/v1.1.1/ImageAnnIcon.png)** is included if you wish to use it for a shortcut to the program.  

---

**Program Description**

The Image Annotator is a program for incorporating simple annotations on an image.  Once a base image is loaded into the program the user can then select to add simple annotations to the image. The program is useful for creating images to be incorporated into course notes, presentations, and other documents.

---

**Screenshot**

![Screenshot of program.](https://github.com/mathprofdes/Image-Annotator/releases/download/v1.1.1/ProgLayout.png)
