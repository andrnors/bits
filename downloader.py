#-----------------------------------------------------------
#
# Web Page Downloader
#
# This simple program is a stand-alone tool to help you
# develop your solution to Assignment 2. For a particular
# URL, it downloads the corresponding web
# page and prints it to the Python shell window.
# You can then examine the HTML/XML source of the document
# and copy parts of it into the "regex tester" to help you
# develop your expressions for extracting particular document
# elements.  This simple script has no user interface or error
# handling, but feel free to add them if you want!
#
# Q: Why not just look at the web page's source in your
# favourite web browser (Firefox, Google Chrome, etc)?
#
# A: Because when a Python script uses the Hyper-Text Transfer
# Protocol to download a web document, it may not receive
# the same file you see in your browser!  Some web servers
# produce different HTML or XML code for different clients.
# Worse, some web servers may refuse to send documents to
# programs other than standard web browsers.  If a Python
# script requests a web document they may instesd respond with
# an "access denied" message.  Therefore, to confirm that the
# HTML code you think is returned by the web server is the
# same code that your own Python program sees you can use
# this script as a test.
#

from urllib import urlopen

url = 'http://www.vg.no/' # Put your web page address here

# Read the contents of the web page as a character string
web_page_contents = urlopen(url).read()

# Display the downloaded web page
print web_page_contents

# At this point you have the Web document as a string,
# so you can put whatever Python code you like here
# to manipulate it, or cut-and-paste the displayed contents
# from IDLE's shell window into some other tool such as
# the "regex tester" or a text editor


