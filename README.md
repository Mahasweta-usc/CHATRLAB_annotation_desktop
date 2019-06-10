# Data Viewer

Data visualizer for browsing/annotation for Instagram Vaccination Misinformation project.

## Getting Started

Download all the files.Extract the folder. 
Execute bash script mac-setup.command by clicking icon and chosing to run in Terminal. Alternatively open a Terminal, change to application directory, and type ./mac-setup.command

### Prerequisites

Install Python 3.7.3 here https://www.python.org/ftp/python/3.7.3/python-3.7.3-macosx10.6.pkg (64/32 bit installer for Mac OSX) or https://www.python.org/ftp/python/3.7.3/python-3.7.3-macosx10.9.pkg (64 bit installer OSX). 
Run the Installer.

### Usage

Annotator launches with initial window to ask user details to keep track of annotators and jobs. Do not leave blank. 
Dashboard has options to browse, delete, skip, and label polarity and misinformation content of posts.
Textbox displays caption, image-text rendering and image tags obtained using Google vision API
Counter to track number of misinformation posts detected
Delete images irrelevant to content, skip if not confident of apt label or content has a mismatch between actual image-text and rendered image-text/image object labels.
Deleted images are stored in a separete bucket and can be retrieved as necessary. 

