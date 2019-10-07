# Data Viewer

Interactive Data visualizer for browsing/annotation for Instagram Vaccination Misinformation project. Requests information from Google cloud storage, stores updated Annotation responses.

## Getting Started

Download all the files. Extract the folder. 
Execute bash script mac-setup.command by clicking icon and chosing to run in Terminal. Alternatively open a Terminal, change to application directory, ex: type cd /home<user>/Downloads/Data_viewer (or your folder path) && ./mac-setup.command

### Prerequisites

Install Python 3.7.3 here https://www.python.org/ftp/python/3.7.3/python-3.7.3-macosx10.6.pkg (64/32 bit installer for Mac OSX) or https://www.python.org/ftp/python/3.7.3/python-3.7.3-macosx10.9.pkg (64 bit installer OSX). 
Run the Installer.

### Usage

Running internet connection required through out. API launch takes some time.
Annotator launches with initial window to ask user details to keep track of annotators and jobs. Do not leave blank. 
Choose unique username to record responses
Dashboard has options to browse (next to browse), delete (irrelevant samples), and label polarity, category and misinformation content of posts.
Textbox displays caption, image-text rendering and information extracted from URLs
Counter to track number of posts labeled by every user.
Delete images irrelevant to content, skip if not confident of appropriate label or content has a mismatch between actual image-text and rendered image-text/image object labels.
Deleted images are stored separately and can be retrieved as necessary. 
Choose between several categories of posts as you may deem relevant. Multiple choices if indicated, are recorded.
Final responses are not recorded until you "submit". Shift between selections of polarity and content label if required before "submitting" final selections. Or use "reset category" to re-enter category choices before submission. 
Interface closes when annnotation of all posts is completed by a user or remaining posts are being viewed by other users. Message is displayed in Terminal accordingly. 
If runtime issues are encountered,open an "issue" thread (GitHub account required) or email repo owner.
