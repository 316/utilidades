#!/usr/bin/env python
#  XMMS2 - X Music Multiplexer System
#  Copyright (C) 2013 Marco Mansilla
# 
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License, or (at your option) any later version.
#                   
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.


#imports for xmms2
import xmmsclient
import os
import sys
#imports for pynotify
import pygtk
pygtk.require('2.0')
import pynotify

#connection settings
xmms = xmmsclient.XMMS("xmmsnotify")

try:
	xmms.connect(os.getenv("XMMS_PATH"))
except IOError, detail:
	print "Connection failed:", detail
	sys.exit(1)

#get current id
result = xmms.playback_current_id()
result.wait()
if result.iserror():
	print "playback current id returns error, %s" % result.get_error()
id = result.value()

if id == 0:
	print "Nothing is playing."
	sys.exit(1)

#getting info from the current song
result = xmms.medialib_get_info(id)
result.wait()

if result.iserror():
	print "medialib get info returns error, %s" % result.get_error()
	sys.exit(1)

#fetching info into variables before printing 
minfo = result.value()
try:
        artist = minfo["artist"]
except KeyError:
	artist = "No Artist"

try:
	title = minfo["title"]
except KeyError:
	title = "No Title"

#call to pynotify for widget generation

NOTIFY_ERRORS=[]

if __name__ == '__main__':
    if not pynotify.init("Basics"):
        sys.exit(1)
 
    n = pynotify.Notification("Now playing \n%s" % artist, "Title: %s" % title)
 
    try:
         n.show()
    except Exception, e:
        NOTIFY_ERRORS.append(e)
    if NOTIFY_ERRORS:
        print "Errors: ", NOTIFY_ERRORS

    sys.exit(1)


