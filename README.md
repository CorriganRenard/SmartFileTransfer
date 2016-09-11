# SmartFileTransfer
Synopsis:
Allows you to select source and destination folder and move text files from the source to the destination based on their last modified date. It will initially use a date 24 hours ago as the cutoff for modified files to transfer. 

When a file is transferred it will create an SQLite database and table and store the date and time of the transfer. 

The program will then use this last date and time for the next file modified cutoff date. 

This program was written with python 3.5

Installation: 
To run you can download the file and run it with IDLE python 3.5
