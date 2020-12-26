
#!/usr/bin/env python

import os, sys, getopt, signal, random, time, warnings

import inspect

from pymenu import  *
from pgui import *

sys.path.append('../pycommon')

from pgutils import  *
from pggui import  *
from pgsimp import  *

import gi
gi.require_version("Gtk", "3.0")
gi.require_version('WebKit2', '4.0')

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib
from gi.repository import GObject
from gi.repository import Pango
from gi.repository import WebKit2

class pgwebw(WebKit2.WebView):

    def __init__(self, xlink=None):
        GObject.GObject.__init__(self)
        self.xlink = xlink

    def do_ready_to_show(self):
        #print("do_ready_to_show() was called")
        pass

    def do_load_changed(self, status):

        #print("do_load_changed() was called", status)
        self.xlink.status.set_text("Loading ... " + self.get_uri()[:64])

        if status == 3: #WebKit2.LoadEvent.WEBKIT_LOAD_FINISHED:
            #print("got WEBKIT_LOAD_FINISHED")
            self.xlink.edit.set_text(self.get_uri()[:64])
            self.xlink.status.set_text("Finished: " + self.get_uri()[:64])
            self.grab_focus()

    def do_load_failed(self, load_event, failing_uri, error):
        print("do_load_failed() was called", failing_uri)
        self.xlink.status.set_text("Failed: " + self.get_uri()[:64])

# EOF