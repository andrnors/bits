
#-----Statement of Authorship----------------------------------------#
#
#  This is an individual assessment item.  By submitting this
#  code I agree that it represents my own work.  I am aware of
#  the University rule that a student must not act in a manner
#  which constitutes academic dishonesty as stated and explained
#  in QUT's Manual of Policies and Procedures, Section C/5.3
#  "Academic Integrity" and Section E/2.1 "Student Code of Conduct".
#
#    Student no: N980506
#    Student name: Andreas Norstein
#
#  NB: Files submitted without a completed copy of this statement
#  will not be marked.  Submitted files will be subjected to
#  software plagiarism analysis using the MoSS system
#  (http://theory.stanford.edu/~aiken/moss/).
#
#--------------------------------------------------------------------#



#-----Task Description-----------------------------------------------#
#
#  Publish Your Own Periodical
#
#  In this task you will combine your knowledge of HTMl/XML mark-up
#  languages with your skills in Python scripting, pattern matching
#  and Graphical User Interface design and development to produce a
#  useful application for publishing a customised newspaper or
#  magazine on a topic of your own choice.  See the instruction
#  sheet accompanying this file for full details.
#
#--------------------------------------------------------------------#



#-----Imported Functions---------------------------------------------#
#
# Below are various import statements that were used in our sample
# solution.  You should be able to complete this assignment using
# these functions only.

# Import the function for opening a web document given its URL.
from urllib import urlopen

# Import the function for finding all occurrences of a pattern
# defined via a regular expression.
from re import findall

# A function for opening an HTML document in your operating
# system's default web browser. We have called the function
# "webopen" so that it isn't confused with the "open" function
# for writing/reading local text files.
from webbrowser import open as webopen

# An operating system-specific function for getting the current
# working directory/folder.  Use this function to create the
# full path name to your publication file.
from os import getcwd

# An operating system-specific function for 'normalising' a
# path to a file to the path naming conventions used on this
# platform.  Apply this function to the full name of your
# publication file so that your program will work on any
# operating system.
from os.path import normpath

# Import the standard Tkinter functions.
from Tkinter import *


# Import the SQLite functions.
from sqlite3 import *

# Import the date/time function.
from datetime import datetime

#
#--------------------------------------------------------------------#



#-----Student's Solution---------------------------------------------#
#
# Put your solution at the end of this file.
#


# Name of the published newspaper or magazine. To simplify marking,
# your program should publish its results using this file name.

#  Initilizes the program, creates the start html
file_name = 'publication.html'

connection = connect(database="internet_activity.db")
database = connection.cursor()

##### GLOBALS #####
date_time_now = "" ## Init as an empty string. Have to do this so the database can write
checkIfPrinted = False  ## Uses this to check if any news are printed

## Storing the links for the database localy
## This is to avoid reading the webpage two times
sportLink = ""
editionLink =""
footballLink =""
europeLink =""
technologyLink =""
travelLink =""

##### GLOBALS END ######


### Sources ###
## By putting everything in functions, it will read an updated version every time you
## you print. This allows users to let the program run, and when they come back articles will be updated it they hit
def GetCnnSport():
    sourceCNNSport = urlopen("http://rss.cnn.com/rss/edition_sport.rss") ## If the chechbox is checked it will find news and downnload them
    CNNSport = sourceCNNSport.read()  ## If the chechbox is checked it will find news and downnload them
    sourceCNNSport.close()
    return CNNSport


def GetCnnEurope():
    sourceCNNEurope = urlopen("http://rss.cnn.com/rss/edition_europe.rss")
    CNNEurope = sourceCNNEurope.read()
    sourceCNNEurope.close()
    return CNNEurope

def GetCnnFootball():
    sourceCNNFootball = urlopen("http://rss.cnn.com/rss/edition_football.rss")
    CNNFootball = sourceCNNFootball.read()
    sourceCNNFootball.close()
    return CNNFootball

def GetCnnEdition():
    sourceCNNEdition = urlopen("http://rss.cnn.com/rss/edition.rss")
    CNNEdition = sourceCNNEdition.read()
    sourceCNNEdition.close()
    return CNNEdition

def GetCnnTechnology():
    sourceCNNTechnology = urlopen("http://rss.cnn.com/rss/edition_technology.rss")
    CNNTechnology = sourceCNNTechnology.read()
    sourceCNNTechnology.close()
    return CNNTechnology

def GetCnnTravel():
    sourceCNNTravel = urlopen("http://rss.cnn.com/rss/edition_travel.rss")
    CNNTravel = sourceCNNTravel.read()
    sourceCNNTravel.close()
    return CNNTravel


### Sources end ###

## Init the head of the new paper
## Writes basic html
def init(file):
    # Basic to create HTML page
    file.write("<!DOCTYPE html>\n")
    file.write('<html lang ="en">\n')
    file.write("<head>\n")

    ## BOOTSTRAP
    file.write("""
    <!-- Latest compiled and minified CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <!-- jQuery library -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <!-- Latest compiled JavaScript -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script
    """)

    file.write('<meta charset="UTF-8">\n')  ## Just charset to normal cars
    file.write("<title> MEGA NEWS </title>\n")
    file.write("</head>\n")
    file.write("<body style='width: 70%; margin: auto;'>\n")

    #  Masthead
    file.write("<div style='text-align:center;' >\n")
    file.write("<h1> MEGA NEWS </h1>\n")
    file.write("<img class='img-rounded' width='500' height = '400' src='data:image/jpeg;base64,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' />\n")
    file.write("<p style='font-weight:bold;'> News for everyone! </p>\n")
    file.write("<hr>\n")
    file.write("</div>\n")

#  uses this to find the different elements I need
#  Makes it easy to scrape the RSS feed
def find(source, first, last):
    try:
        start = source.index(first) + len(first)
        end = source.index(last, start)
        return source[start:end]
    except ValueError:
        return ""

##  This function finds all the sources that are needed
def findNewsArticle(source):
    ''':returns [title, description, link, publicationDate, picture'''

    ## Makes it posible to edit global variables
    global sportLink
    global editionLink
    global footballLink
    global  travelLink
    global europeLink
    global technologyLink

    ## need this to check which of the links I should edit
    sourceTitle = find(source, "<channel>", "</title>")  ## This will never change. This is the title of the channel. That's why I can use it

    item = find(source, "<item>", "</item>")  #  Find the newest news article the RSS feed

    title = find(item, "<title>", "</title>")  #  Gets the title
    if "<![CDATA[" in title:  #  If the title contains this it removes it. (This is specific to some of the titles in CNN's RSS feed
        title = find(item, "<title><![CDATA[", "]]></title>")

    link = find(item, "<link>", "</link>")  # Finds the link to the article


    description = find(item, "<description>", "</description>")  # Find description
    if description == "":
        ## If the RSS FEED does not have a description tag, I'll open the link and find the Story Highlights of the article there.
        ## All articles from CNN have that
        newSource = urlopen(link).read()
        matches = findall('<li class="el__storyhighlights__item el__storyhighlights--normal">(.*)</ul>', newSource)
        for line in matches:
            description = line[:line.index("</li>")]


    if "<![CDATA[" in description:  #  Same check as with title
        description = find(item, "<description><![CDATA[", "]]></description>")
    if "&lt;" in description and description.index("&") == 0:  ### CNN does not provide a Description to every article in their RSS feeds. The article is still there, but may not be a description
        # description = "No descripiton provided by CNN, please click the link below to read the full article. "  ## Tells the user that there are no description, and link to the full article
        ## If the RSS FEED does not have a description between description tags, I'll open the link and find the Story Highlights of the article there.
        ## All articles from CNN have that
        newSource = urlopen(link).read()
        matches = findall('<li class="el__storyhighlights__item el__storyhighlights--normal">(.*)</ul>', newSource)
        for line in matches:
            description = line[:line.index("</li>")]

    elif "&lt;" in description: # Removes trash link from end of description
        stopPoint = description.index("&lt;")
        description = description[0 : stopPoint]

    publicationDate = find(item, "<pubDate>","</pubDate>")  ## finds the publication date
    picture = find(item, 'url="', '"')  # only URL tag is in images, so this will work

    ## Checks the which link it should update
    ## Exploits parts of static channel names
    if "Travel" in sourceTitle:
        travelLink = link
    elif "Europe" in sourceTitle:
        europeLink = link
    elif "Football" in sourceTitle:
        footballLink = link
    elif "Homepage" in sourceTitle:
        editionLink = link
    elif "Technology" in sourceTitle:
        technologyLink = link
    else:
        sportLink = link

    return [title, description, link, publicationDate, picture]  # returns information as a list

##  This function write a new article
def writeNewsArticle(source, category, file):
    ## This strings converts the datetime object to a string an slices the string so it shows preciseness to seconds
    global date_time_now ## makes it posible to edit the global variable
    date_time_now = str(datetime.now())[:-7]

    news = findNewsArticle(source)  ## finds the article
    file.write("<p style='text-align:center; font-weight:bold;'>" + category + "</p>")  ## Writes the category
    file.write("<h2 style='text-align:center;'>" + news[0] + "</h2>\n")  ## Writes the title
    file.write("<img class='img-rounded' src ='" + news[4] + "'/>\n")  ## Writes the image
    file.write("<p style='width:60%;'>" + news[1] + "</p>\n")  ## Writes the description
    file.write("<a href ='" + news[2] + "' target='blank'>" + "See full article" + "</a>\n")  ## Writes the link
    file.write("<p> Publication date: " + news[3] + "</p>\n")  ## writes the publication date
    file.write("<p> Article fetched: " + date_time_now + "</p>\n")
    file.write("<hr>")  ## Creates a line to divide news from each other


##### GUI STARTS HERE #####

window = Tk()  ## creates window
window.title("MEGA NEWS GENERATOR")  ## Sets the tilte
window.configure(background="#1abaff")  ## Background color
window.geometry("1000x450")  # Size of window

## Command for print button
## The HTML file is created here and all writing is done in this method
def printCommand():
    global checkIfPrinted
    checkIfPrinted = False  ## Boolean to check if anything is printed. This is to validate, so users cannot push empty
    text.delete("1.0", END) ## Empties text field for every print
    with open("publication.html", "w") as file:
        init(file) ## Starts writing
        if checkSport.get() == True:  ## Checks if th checkbox is checked. This is the same check for every "if-sentence"
            text.insert(END, "Printing Sport News\n")  ## Shows progress to user
            writeNewsArticle(GetCnnSport(), "Sport", file)  ## Then write the news to the html file, CNN SPORT is defind at the top
            checkIfPrinted = True

        ## Se comments over, each check does the same
        ## Important to check every box, that is why there is only IF and not elif else
        if checkEurope.get() == True:
            text.insert(END, "Printing Europe News\n")
            writeNewsArticle(GetCnnEurope(), "Europe", file)
            checkIfPrinted = True


        if checkFootball.get() == True:
            text.insert(END, "Printing Football News\n")
            writeNewsArticle(GetCnnFootball(), "Football", file)
            checkIfPrinted = True


        if checkNews.get() == True:
            text.insert(END, "Printing Top News News\n")
            writeNewsArticle(GetCnnEdition(), "Top News", file)
            checkIfPrinted = True


        if checkTech.get() == True:
            text.insert(END, "Printing Technology News\n")
            writeNewsArticle(GetCnnTechnology(), "Technology", file)
            checkIfPrinted = True


        if checkTravel.get() == True:
            text.insert(END, "Printing Travel News\n")
            writeNewsArticle(GetCnnTravel(), "Travel", file)
            checkIfPrinted = True

        ## Ends the HTML file
        text.insert(END, "Done!\n")
        file.write("</body>\n")
        file.write("</html>\n")

## This method is invoked when the launch button is pressed
## Opens the the HTML file in browser
## NB: Works on Linux and Windows, NOT tested for Mac
def launchCommand():
    url = "publication.html"
    webopen(url, new = 2)

## This method is invoked when the launch button is pressed
## This method writes content to the database
def recordCommand():
    if checkIfPrinted:
        count_rows = database.execute("SELECT COUNT(*) FROM Recent_Downloads").fetchone()[0]  ## Counts rows in table
        if count_rows > 0:  ## checks it table is empty
            database.execute("DELETE FROM Recent_Downloads;")  ## if it is not empty, I'll empty it


        if checkSport.get() == True:  ## Checks if the checkbox is checked. This is the same check for every "if-sentence"
            database.execute("INSERT INTO Recent_Downloads VALUES ('" + date_time_now  + "' , " + "'" + sportLink + "')")  ## inserts data into database (dateTime, urlToArticle)

        ## Se comments over, each check does the same
        ## Important to check every box, that is why there is only IF and not elif else
        if checkEurope.get() == True:
            database.execute("INSERT INTO Recent_Downloads VALUES ('" + date_time_now  +"'," + "'" + europeLink + "')")

        if checkFootball.get() == True:
            database.execute("INSERT INTO Recent_Downloads VALUES ('" + date_time_now  + "'," + "'" + footballLink + "')")

        if checkNews.get() == True:
            database.execute("INSERT INTO Recent_Downloads VALUES ('" + date_time_now  +"'," + "'" + editionLink + "')")

        if checkTech.get() == True:
            database.execute("INSERT INTO Recent_Downloads VALUES ('" + date_time_now  +"'," + "'" + technologyLink + "')")

        if checkTravel.get() == True:
            database.execute("INSERT INTO Recent_Downloads VALUES ('" + date_time_now  +"'," + "'" + travelLink + "')")

        text.insert(END, "News paper saved to database \n")

        # print "SUCCESS"
        connection.commit()
    else:
        text.insert(END, "YOU HAVE NOT SELECTED ANY NEW TO SAVE \n")
        text.insert(END, "PLEASE CHECK SOME OF THE BOXES ON THE RIGHT SIDE \n")


# To check checkbutton state
checkNews = IntVar()
checkSport  = IntVar()
checkTech = IntVar()
checkFootball = IntVar()
checkTravel = IntVar()
checkEurope = IntVar()

# Creates checkbuttons
CheckbuttonNews = Checkbutton(window, text = "Top News", variable = checkNews, onvalue = 1, offvalue = 0, height=5, width = 20, bg ="#1abaff", activebackground="#008fcd", bd=0, highlightthickness=0, relief='ridge')
CheckbuttonSport = Checkbutton(window, text = "Sport News", variable = checkSport, onvalue = 1, offvalue = 0, height=5, width = 20, bg ="#1abaff",activebackground="#008fcd",bd=0, highlightthickness=0, relief='ridge')
CheckbuttonTech = Checkbutton(window, text = "Tech News", variable = checkTech, onvalue = 1, offvalue = 0, height=5, width = 20, bg ="#1abaff", activebackground="#008fcd", bd=0, highlightthickness=0, relief='ridge')
CheckbuttonFootball = Checkbutton(window, text = "Football News", variable = checkFootball, onvalue = 1, offvalue = 0, height=5, width = 20, bg ="#1abaff", activebackground="#008fcd", bd=0, highlightthickness=0, relief='ridge')
CheckbuttonTravel = Checkbutton(window, text = "Travel News", variable = checkTravel, onvalue = 1, offvalue = 0, height=5, width = 20, bg ="#1abaff", activebackground="#008fcd", bd=0, highlightthickness=0, relief='ridge')
CheckbuttonEurope = Checkbutton(window, text = "Europe News", variable = checkEurope, onvalue = 1, offvalue = 0, height=5, width = 20, bg ="#1abaff", activebackground="#008fcd", bd=0, highlightthickness=0, relief='ridge')

# Creates label to text filed
progressText = StringVar()
progressLabel = Label(window, textvariable = progressText, bg="#1abaff", font=("Serif, 12"))
progressText.set("Click print and progress will be displayed in window below")


# Creates text filed
text = Text(window, height = 15,  wrap= WORD, bg = "#67d1ff")

#Creates buttons
buttonPrint = Button(window, text = "Print", width = 5, command = printCommand, bg="#1aff5f", activebackground="#10ff22")
buttonLaunch = Button(window, text = "Open MEGA NEWS", width = 15, command = launchCommand, bg="#1aff5f", activebackground="#10ff22")
buttonRecord = Button(window, text= "Record", width="10", command = recordCommand, bg="#1aff5f", activebackground="#10ff22")

# Adds everything to the grid
marginSize = 4
CheckbuttonNews.grid(pady = marginSize, row = 0, column =2)
CheckbuttonSport.grid(pady = marginSize, row = 0, column =3)
CheckbuttonTech.grid(pady = marginSize, row = 1, column =2)
CheckbuttonFootball.grid(pady = marginSize, row = 1, column =3)
CheckbuttonTravel.grid(pady = marginSize, row = 2, column =2)
CheckbuttonEurope.grid(pady = marginSize, row = 2, column =3)
progressLabel.grid(column = 0, row = 0)
text.grid(pady = marginSize+10, row = 1, column = 0, columnspan = 2)
buttonPrint.grid(pady=marginSize, row = 2, column = 1)
buttonLaunch.grid(pady=marginSize, row = 2, column = 0)
buttonRecord.grid(pady=marginSize, row = 3, column = 0)


# Starts the program
window.mainloop()

## Closes the database connection
## By closing it here, you can do more then one "print" each time you run the program

database.close()
connection.close()

