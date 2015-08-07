#!/usr/bin/python3

# -*- coding: UTF-8 -*-

import cgi
import cgitb; cgitb.enable()
import cdp

print('Content-Type: text/html')
print('')

arguments = cgi.FieldStorage()

print("")

cdp = cdp.cdp(arguments['cdpserver'].value, '9443', 'admin', 'password')

cdp.run(arguments['hostname'].value, arguments['ip'].value, 1167, arguments['os'].value, arguments['schehours'].value, arguments['freqhours'].value)

print("<br/><br/><b>DONE</b>")
