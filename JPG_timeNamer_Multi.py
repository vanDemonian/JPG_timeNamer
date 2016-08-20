#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
Filename:       JPG_timeNamer_Multi.py
Author:         Martin Walch
Release Date:   2016-04-14

Description:    A faster version of the earlier JPG_timeNamer.py
                This version rquires that the namimg string be input manually into this file.
                Unlike the earlier version, it does not attempt to ascribe location according
                to the camera serial number.


                location = 7 character string


                Iterates through a directory tree, reading the EXIF data from each JPG. Parses the
                date/time and camera Serial Number from EXIF data, reNames the files according to a
                list ofcamera locations and the date/time the image was digitised. 
                Then copies the photo and uses the date/time value to save in a new camera/year/month
                based directory tree. 

                Additional sort outputs by day available - see dateSort variable.              

Attributions:   Ideas and code borrowed from Alex Harden's PhotoLibrarian.py:
                http://code.activestate.com/recipes/511439
                Chad Cooper's RenameCopyPhotos.py:
                http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/500266

                EXIF.py: http://sourceforge.net/projects/exif-py/
                Dirwalk.py borrowed from the ActiveState Python Cookbook:
                http://code.activestate.com/recipes/105873/
---------------------------------------------------------------------------------------------------
"""

import glob
from PIL import Image
from PIL import ImageStat
from PIL import ImageChops
from PIL.ExifTags import TAGS, GPSTAGS
import string, sys, traceback, datetime, time, calendar
import EXIF, os, shutil
import dirwalk
from PIL import *
from multiprocessing import Pool

#  N.B.    location must be a 7 character string only
location  = 'KINGWIL'

inputDir = '/Users/pyDev/Documents/JPG_TIMESLICERY/JPG_TimeSlice_Multi/input/107LKW2'          #root directory that will be parsed (includes subdirectories)
myOutputDir = '/Users/pyDev/Documents/JPG_TIMESLICERY/JPG_TimeSlice_Multi/JPG_timeNamer_Outputs'            #output directory (should be present before script is run)
fileExt = '.JPG'                                                        #restrict to JPGs (we need EXIF data)

                                                          
pictureList = dirwalk.dirwalk(inputDir)
print pictureList
count = 0

def FilePic((myPicture)):
    """
    Files the specified picture in the OutputDir according to EXIF Camera Model and date:
    /myOutputDir
        /<EXIF Camera serial number conerted to location name>
            /<year>
                /<month>
                    /<day>  (optional)
                        /<myPicture>
    """





    try:
        f=open(myPicture, 'rb')
        tags=EXIF.process_file(f)
        myFilename=os.path.basename(myPicture)

        datestr = str(tags['EXIF DateTimeDigitized'])
        

        datestr = datestr.split(' ')
        dt = datestr[0]  # date
        tm = datestr[1]  # time
        # Date
        y = dt.split(':')[0]    # year
       
        if len(dt.split(':')[1]) < 2:   # month
            m = str('0') + dt.split(':')[1] 
        else:
            m = dt.split(':')[1]
           
        if len(dt.split(':')[2]) < 2:   # day
            d = str('0') + dt.split(':')[2] 
        else:
            d = dt.split(':')[2]

        # Time
        h = tm.split(':')[0]  # hour
        min = tm.split(':')[1]  # minute
        s = tm.split(':')[2]  # second

        # Establish new filename in form of:
        # yyyy-mm-dd_hh-mm-ss.jpg
        newName = location + '_' + dt.replace(':','_') + '-' + tm.replace(':','_') + '.jpg'
        myFilename = newName

        # Check for/make dirs for file to go into
        # If dir already exists, use it - if it doesn't exist, then create it

        if os.path.isdir(myOutputDir) != 1:
            os.mkdir(myOutputDir)
        if os.path.isdir(myOutputDir + '/' + location) != 1:
            os.mkdir(myOutputDir + '/' + location)
        if os.path.isdir(myOutputDir + '/' + location + '/' + y) != 1:
            os.mkdir(myOutputDir + '/' + location + '/' + y)
        if os.path.isdir(myOutputDir + '/' + location + '/' + y + '/' + m) != 1:
            os.mkdir(myOutputDir + '/' + location + '/' + y + '/' + m)
 

        # Copy file, renaming it with new filename

        myNewFilePath=myOutputDir + '/' + location + '/' + y + '/' + m + '/' + myFilename

        print 'New File: %s' % (myNewFilePath)

        shutil.copyfile(myPicture,myNewFilePath)
            

        # Set modified time to date photo was digitized
        myCurrentTime = datetime.datetime.now()
        myCurrentTime = int(time.mktime(myCurrentTime.timetuple()))
        myDigitizedTime = datetime.datetime(int(y), int(m), int(d), int(h), int(min), int(s))
        myDigitizedTime = int(time.mktime(myDigitizedTime.timetuple()))
        myTimes=(myCurrentTime,myDigitizedTime)
        os.utime(myNewFilePath,myTimes)
    except:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        pymsg = "PYTHON ERRORS:\nTraceback Info:\n" + tbinfo + "\nError Info:\n    " + \
            str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"




def Timer(start, end):
    """
    Calculates the time it takes to run a process, based on start and finish times
    ---------------------------------------------------------------------------------------------
    Inputs:
    start:        Start time of process
    end:          End time of process
    ---------------------------------------------------------------------------------------------
    """
    elapsed = end - start
    # Convert process time, if needed
    if elapsed <= 59:
        time = str(round(elapsed,2)) + " seconds\n"
    if elapsed >= 60 and elapsed <= 3590:
        min = elapsed / 60
        time = str(round(min,2)) + " minutes\n"
    if elapsed >= 3600:
        hour = elapsed / 3600
        time = str(round(hour,2)) + " hours\n"
    return time





##### RUN #####

if __name__ == '__main__':
    start = time.clock()

    print '   '
    print 'Running JPG_timeNamer_Multi.py   '
    print '   '

    # pool.map(func, list) does same job as this for loop
    # 
    # for picture in pictureList:

        # FilePic(picture)
        # count = count + 1




    pool = Pool()

    pool.map(FilePic, pictureList)




    pool.close() 
    pool.join()






    finish = time.clock()
    print '\nProcessing done in ', Timer(start, finish)





