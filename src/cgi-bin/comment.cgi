#!/usr/local/bin/python

import cgi
import cgitb

cgitb.enable()

form = cgi.FieldStorage()
text = form.getfirst("text", "")
author = form.getfirst("author", "")
id = form.getfirst("id", "")

import smtplib
server = smtplib.SMTP('localhost')
server.sendmail('dado1945@uosis.mif.vu.lt', 'dalius.dobravolskas@gmail.com', text[:2048])
server.quit()
