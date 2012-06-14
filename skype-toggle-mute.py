#!/usr/bin/env python
# http://forum.skype.com/index.php?showtopic=480701

import time
import gobject

import dbus, sys
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop

VERBOSE = False

class Skype() :
  def __init__(self) :
    remote_bus = dbus.SessionBus(mainloop=DBusGMainLoop(set_as_default=True))

    system_service_list = remote_bus.get_object('org.freedesktop.DBus', '/org/freedesktop/DBus').ListNames()
    skype_api_found = 0

    for service in system_service_list:
      if service == 'com.Skype.API':
        skype_api_found = 1
        break

    if not skype_api_found:
      sys.exit('No running API-capable Skype found')

    self.skype_api_object = remote_bus.get_object('com.Skype.API', '/com/Skype')

    answer = self.send_dbus_message('NAME SkypeApiPythonTestClient')
    if answer != 'OK':
      sys.exit('Could not bind to Skype client')

    if VERBOSE :
      print "OK:", answer

    answer = self.send_dbus_message('PROTOCOL 7')
    if VERBOSE :
      print "PROTOCOL 7:", answer

    if answer != 'PROTOCOL 7':
      sys.exit('This test program only supports Skype API protocol version 7')

  def skype_toggle_mute(self) :
    answer = self.send_dbus_message('GET MUTE')
    if VERBOSE :
      print "GET MUTE:", answer

    if answer == 'MUTE ON' :
      answer = self.send_dbus_message('SET MUTE OFF')
      if VERBOSE :
        print "SET MUTE OFF:", answer
    else :
      answer = self.send_dbus_message('SET MUTE ON')
      if VERBOSE :
        print "SET MUTE ON:", answer

  # Client -> Skype
  def send_dbus_message(self, message):               
    response = self.skype_api_object.Invoke(message)
    return response

if __name__ == "__main__":
  s = Skype()
  s.skype_toggle_mute()
