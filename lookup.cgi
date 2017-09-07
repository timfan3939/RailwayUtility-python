#!/usr/bin/env python3

import cgi

import cgitb
cgitb.enable()

def main():
	print('Content-Type: text/html\n\n')

	form  = cgi.FieldStorage()
	if 'name' not in form or 'addr' not in form:
		print('<H1>Error</H1>')
		print('Name or Address do not exist in form')
		return

	print('Name: {}<br />'.format(form['name'].value))
	print('Address: {}<br />'.format(form['addr'].value))

if __name__ == '__main__':
	main()


