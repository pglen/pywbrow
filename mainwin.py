#!/usr/bin/env python

import os, sys, getopt, signal, random, time, warnings

import inspect

from pymenu import  *
from pgui import *

realinc = os.path.realpath(os.path.dirname(__file__) + os.sep + "../pycommon")
sys.path.append(realinc)

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

try:
    import pgwkit
except:
    print("Please install WebKit2", __file__, __line__)
    #sys.exit(1)

def func():
    pass

# ------------------------------------------------------------------------

class MainWin(Gtk.Window):

    def __init__(self, conf, args):

        Gtk.Window.__init__(self, Gtk.WindowType.TOPLEVEL)
        #self = Gtk.Window(Gtk.WindowType.TOPLEVEL)
        register_stock_icons()
        self.set_title("Python Webkit Browser")
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)

        #ic = Gtk.Image(); ic.set_from_stock(Gtk.STOCK_DIALOG_INFO, Gtk.ICON_SIZE_BUTTON)
        #window.set_icon(ic.get_pixbuf())

        self.fname = os.path.dirname(__file__) + os.sep + "home.html"
        www = Gdk.Screen.width(); hhh = Gdk.Screen.height();

        disp2 = Gdk.Display()
        disp = disp2.get_default()
        #print( disp)
        scr = disp.get_default_screen()
        ptr = disp.get_pointer()
        mon = scr.get_monitor_at_point(ptr[1], ptr[2])
        geo = scr.get_monitor_geometry(mon)
        www = geo.width; hhh = geo.height
        xxx = geo.x;     yyy = geo.y

        # Resort to old means of getting screen w / h
        if www == 0 or hhh == 0:
            www = Gdk.screen_width(); hhh = Gdk.screen_height();

        if www / hhh > 2:
            self.set_default_size(5*www/8, 7*hhh/8)
        else:
            self.set_default_size(7*www/8, 7*hhh/8)

        self.connect("destroy", self.OnExit)
        self.connect("key-press-event", self.key_press_event)
        self.connect("button-press-event", self.button_press_event)
        #self.connect("button-press-event", self.motion)

        iconfile = os.path.dirname(__file__) + os.sep + "assets" + os.sep + "browser.png"
        try:
            self.set_icon_from_file(iconfile)
        except:
            print("Cannot set icon", iconfile)
            pass

        vbox = Gtk.VBox();
        merge = Gtk.UIManager()
        #self.mywin.set_data("ui-manager", merge)

        aa = create_action_group(self)
        merge.insert_action_group(aa, 0)
        self.add_accel_group(merge.get_accel_group())

        merge_id = merge.new_merge_id()

        try:
            mergeid = merge.add_ui_from_string(ui_info)
        except GLib.GError as msg:
            print("Building menus failed: %s" % msg)


        bbox = Gtk.VBox()
        self.mbar = merge.get_widget("/MenuBar")
        self.mbar.show()

        self.tbar = merge.get_widget("/ToolBar");
        self.tbar.show()

        bbox.pack_start(self.mbar, 0,0, 0)
        bbox.pack_start(self.tbar, 0,0, 0)

        if not conf.kiosk:
            vbox.pack_start(bbox, False, 0, 0)

        #hbox2 = Gtk.HBox()
        #lab3 = Gtk.Label("");  hbox2.pack_start(lab3, 0, 0, 0)
        #lab4 = Gtk.Label("");  hbox2.pack_start(lab4, 0, 0, 0)
        #vbox.pack_start(hbox2, False, 0, 0)

        #urlbar = self.create_urlbar()
        #if not conf.kiosk:
        #    vbox.pack_start(urlbar, False, False, 2)

        self.notebook_1 =  Gtk.Notebook.new();
        #notebook.size_allocate(Gdk.Rectangle(0, 0, 10,10))
        #notebook.popup_enable()
        self.notebook_1.set_scrollable(True)

        self.notebook_1.append_page(self.create_browwin(), self.makelabel("test"))
        self.notebook_1.append_page(self.create_browwin())

        #webview.load_uri("https://google.com")
        #self.webview.load_uri("file://" + self.fname)
        #if not args:
        #    self.baseurl(None, None, None)
        #else:
        #    self.go(args[0])

        #browse_win.add(self.notebook_1)
        vbox.pack_start(self.notebook_1, 1, 1, 2)

        #hbox4 = Gtk.HBox()
        #lab1 = Gtk.Label("");  hbox4.pack_start(lab1, 1, 1, 0)
        #lab2 = Gtk.Label("  ");  hbox4.pack_start(lab2, 0, 0, 0)
        #butt1 = Gtk.Button.new_with_mnemonic(" _New ")
        ##butt1.connect("clicked", self.show_new, window)
        #hbox4.pack_start(butt1, False, 0, 2)
        #butt2 = Gtk.Button.new_with_mnemonic(" E_xit ")
        #butt2.connect("clicked", self.OnExit, self)
        #hbox4.pack_start(butt2, False, 0, 0)
        #vbox.pack_start(hbox4, False, 0, 6)

        hbox5 = Gtk.HBox()
        hbox5.pack_start(Gtk.Label("  "), 0, 0, 0)
        self.status = Gtk.Label(" Idle ");
        self.status.set_xalign(0)
        hbox5.pack_start(self.status, 1, 1, 0)
        hbox5.pack_start(Gtk.Label("  "), 0, 0, 0)

        if not conf.kiosk:
            vbox.pack_start(hbox5, False, 0, 6)

        if conf.kiosk:
            self.fullscreen()

        self.add(vbox)
        self.show_all()

        self.set_status(" Idle State ")

        #print(dir(self.webview))
        #print(self.webview.__dict__)

        # Original
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Safari/605.1.15"

        settings = self.webview.get_settings()

        settings.set_enable_encrypted_media(True)
        settings.set_enable_developer_extras(True)
        settings.set_user_agent("Mozilla/5.0 (X11; Linux x86_64; rv:20.0) Gecko/20100101 Firefox/91.0")

        print("User Agent", settings.get_user_agent())

        self.webview.set_editable(True)
        #self.webview.get_settings().set_property("enable_developer_extras", True)

        #for aa in dir(settings):
        #    ppp = ""
        #    if "get" in aa:
        #        try:
        #            zzz = getattr(settings, aa)
        #            if type(zzz) == "str":
        #                ppp = zzz
        #            else:
        #                ppp = zzz()
        #        except:
        #             ppp = "No Prop"
        #        print(aa, "=", ppp)

        '''
        warnings.simplefilter("ignore")
        for aa in dir(settings):
            ppp = ""
            if "list_properties" in aa:
                continue;
            if "__" in aa:
                continue;
            try:
                zzz = getattr(settings, aa)
                if type(zzz) == "str":
                    ppp = zzz
                else:
                    ppp = zzz()
            except:
                 ppp = "No Propx"

            print(aa, "=", ppp)
        warnings.simplefilter("default")
        '''

        #print(settings.get_properties())

        self.webview.editor = self.webview
        self.ui = pgwkit.generate_ui(self.webview)

        self.add_accel_group(self.ui.get_accel_group())
        #self.toolbar1 = self.ui.get_widget("/toolbar_main")
        #self.menubar = self.ui.get_widget("/menubar_main")
        #bbox.pack_start(self.menubar, False, False, 0)
        #bbox.pack_start(self.toolbar1, False, False, 0)
        #bbox.pack_start(self.toolbar2, False, False, 0)


    def makelabel(self, labstr, callb = None):

        label = Gtk.Label.new(labstr)
        label.set_tooltip_text(labstr)
        label.set_single_line_mode(True)

        eb = Gtk.EventBox(); eb.add(label)
        if callb:
            eb.connect_after("button-press-event", Gtk)

        eb.set_above_child(True)

        image = Gtk.Image()
        image.set_from_stock(Gtk.STOCK_CLOSE, Gtk.IconSize.MENU)
        butt = Gtk.Button();  butt.add(image)
        butt.set_focus_on_click(False)
        butt.set_relief( Gtk.ReliefStyle.NONE)

        #butt.connect("clicked", self.close_button)
        butt.set_tooltip_text("Close '%s'" % os.path.basename(self.fname))
        hbox = Gtk.HBox()
        hbox.pack_start(eb, 0, 0, 0)
        hbox.pack_start(butt, 0, 0, 0)
        hbox.show_all()
        return hbox

    def create_browwin(self):

        try:
            #self.webview = pgwkit.pgwebw(self)
            self.hedit = pgwkit.HtmlEdit(True, self.set_status)
            self.webview =  self.hedit._htmlx

        except:
            print(sys.exc_info())
            print("Please install webkit2")
            put_exception("window cration")

            sys.exit(1)
            #self.webview = pgwkit.pgwebw_fake()

        return self.hedit


    def set_status(self, xtxt):
        self.status.set_text(xtxt)

    def  OnExit(self, arg, srg2 = None):
        self.exit_all()

    def exit_all(self):
        Gtk.main_quit()

    def key_press_event(self, win, event):
        #print( "key_press_event", win, event)
        pass

    def button_press_event(self, win, event):
        #print( "button_press_event", win, event)
        pass

    def activate_action(self, action):

        #dialog = Gtk.MessageDialog(None, Gtk.DIALOG_DESTROY_WITH_PARENT,
        #    Gtk.MESSAGE_INFO, Gtk.BUTTONS_CLOSE,
        #    'Action: "%s" of type "%s"' % (action.get_name(), type(action)))
        # Close dialog on user response
        #dialog.connect ("response", lambda d, r: d.destroy())
        #dialog.show()

        #warnings.simplefilter("ignore")
        strx = action.get_name()
        #warnings.simplefilter("default")

        print ("activate_action:", strx)

        if str == "Copy":
            print("copy")

        if str == "Save":
            print("save")

    def activate_quit(self, action):
        print( "activate_quit called")
        self.OnExit(False)

    def activate_exit(self, action):
        print( "activate_exit called" )
        self.OnExit(False)

    def activate_about(self, action):
        print( "activate_about called")
        pass


# Start of program:

if __name__ == '__main__':

    #mainwin = MainWin()
    #Gtk.main()
    pass

# EOF
