Welcome to the README file for the Campus Learning Centers Drop-In scheduler!

In this file, we will go over the following
- Usage
- Installation
- How it works
    - app.py
    - db.py
    - DDL.sql
    - templates
    - deliverables
- Migrate online?
- Contact

## Installation

In this section, I will walk you through the process of installing this program.
you will need the following
    - the **git** command line tool
    - python 3
    - privileges to run a .sh or .bat file
    - privileges to create a venv

- start by cloning this repository:
    git clone https://github.com/shieldsnoahm17/campuslearningcenter.git
- navigate to the repository
    cd campuslearningcenter
- run the .sh file if you are using MacOS/LINUX and the .bat file if you are on Windows
    sh mac_run.sh
    ./windows_run.bat
This will open a terminal, create a venv if you dont have one, activate the venv, download any required repositories
and start the app
The script **should** automatically open a browser, but if it doesnt, simply navigate to your browser of choice and
go your localhost port 5000 by using this URL
    http://127.0.0.1:5000/
- To close the app, just exit the termial, or navigate to the termial and click **ctrl + C**



## Usage

In this section, we will talk about what how to use this app

Currently, This app is meant to be used locally only. It can be put online with ease though, please navigate to the 
bottom to the "Migrate online?" section

To begin, login using the username **admin** and the password **123**
    this must be done in order to access the rest of the app, this isnt really an important feature for an offline
    version, however it is useful once it has a valid IP
    The app will automatically look for a file called /deliverables/oldData.txt, which will contain any previous data
    from the last time it ran, this is a seemless way to resume your session without it being online.

You are now prompted with many selections:
- "Home" just beings you to a page that says welcome
- "Login" allows you to login
- "logout" logs you out (not currently being used for the offline version of the app)
- "selections" beings you to a page with the following choices:
    - "Erase All Data" will clear all saved data and save it as /deliverables/deletedData.txt as a backup
    - "Create Table" will save all data to /deliverables/oldData.txt and create both the internal and external 
        schedules and same them in the /deliverables directory
    - "Scan for Old Data" is used to manually check for /deliverables/oldData.txt and resume that session.
        **This is only done automatically when you login**, if you close the app and restart it without logging back in,
        your data will not be there, this button should load all of that in.
    - "Insert" is used to insert tutors, courses, expertise, availabilities, users, or existing data
        - tutors are identified by a name, and automatically lowercased
        - courses **must** be identified with 4 letters and 3 numbers, it is automatically captitalized
        - Expertise is the pairing of tutors and courses
        - availabilities is the pairing of days, times, and tutors
        - users are the usernames and passwords that have access to the app 
            This is not currently working as it is really only useful when it available to the public
        - Existing data is used as a third layer of security for losing your data. It will take in a CSV (semi-colon, not comma)
            and load that data into your session. This would be a string of characters such as:
            bubba;bubba;{'CMSC303'};{('sunday', '9')};
            This is what you will find in deletedData.txt and oldData.txt, so if you paste your oldData.txt into another file as a 
            backup, you can so that if something currupts, you can simply restore everything by copying and pasting it into "Existing Data"
    - "View" is used to see what data is currently loaded into your session, this can also be seen by looking at the schedules, but
        This is often more convinent
        - "tutor" shows every class each tutor teaches, and what times they teach at
        - "course" shows you who teaches every course, and what times each course is taught
    - "Update" is used to change the courses or availabilities of a tutor
        - "expertise" allows you to give a tutor a new set of expertises, this will overwrite the previous set
        - "availability" allows you to give a tutor a new set of availabilities, this will overwrite the previous set
    - "Delete" is used to delete a Tutor, course, or user
        - "tutor" will delete a tutor, and all of their attributes
        - "course" will delete a course, and remove it from any tutor that has it as an expertise
        - "user" deletes a user from accessing the app (not built for the offline version)


## How it works

In this section, we will talk about the major working component in each file and directory in the repository

- deliverables/ contains the things you want... The internal and external schedules, oldData.txt, and deletedData.txt
- templates contains all the pure HTML
- mac_run.sh and windows_run.bat are used to automatically run the app
- ddl.sql is the DDL for a MySQL database that is needed if the app is to incorporate one
- README.txt is this file lol 
- requirements.txt contains all the dependencies needed to run the app, this is downloaded when first opening the app
- db.py is a subclass of the mysql.connetor connection class. It includes custom functions that can be used to 
    insert, delete, update, select, and run custom queries with ease. 
    - this is only used for an online version
- app.py is the meat and potatos of the application, it has all of the flask routes, helper functions, WTF form classes, etc
    that allows the applcaition to run how it does. There are three main data structures that are used to store and parse the 
    data in a way that makes it easy to understand. They are a bit hard to follow, so here is a breakdown of them:
    - **tutors**: this is a dictionary of Tutor objects where the key is the tutor name, and the value is a Tutor object
        The Tutor object is described below:
        - .name is the name of the tutor
        - .courses is a set of strings that represent the courses a tutor has an expertise in {'CMSC101','CMSC303','MATH100'}\
        -.availabilities is a set of (date, time) tuples that represent the times they can work {(monday, 13),(monday, 14),(tuesday, 8)}
            - This means they are available to work monday from 1pm - 3pm and tuesday 8am - 9am
        - **NOTE**: it is redundant to have name as the key and in the Tutor object, but the key was originally a Vnumber, or something
            that can uniquely identfy them. However this was replaced with name for security issues
    -**all_courses** is used whenever we want to know something about a class but not a tutor. mainly used for the external schedule
        It is a dictionary of subjects (such as "CMSC" or "STAT") in which each subject has a dictionary of course numbers (such as "101")
        in which each course number has a set of times when that course is taught, it looks like this:
        {'CMSC': 
            {'303': 
                {
                ('monday', '10'), 
                ('monday', '9')}}, 
        'BIOL': 
            {'100': 
                {
                ('sunday', '9')}
            }
        }
        - In this example, there are two courses
            - CMSC303 which is taught on Monday from 9am - 11am
            - BIOL100 which is taught on sunday from 9am - 10am
    -**parsedData** Is used in a simlar way as all_courses is used, however it includes data about specific tutors. So it not only has data
        about when a class is taught, but also by who at what times. It has a similar format to all_courses, but instead of a simple set of 
        times, it is a list of tuples, which have a tutor, and the time they teach that class. Here is an example using the same data as above:
        {'BIOL': 
            {'100': 
                [
                    ('bubba', {
                        ('sunday', '9')
                    })
                ]
            }, 
        'CMSC': 
            {'303': 
                [
                    ('chris', {
                        ('monday', '10'), 
                        ('monday', '9')
                    })
                ]
            }
        }
        - We can see here that "bubba" teaches BIOL100 on sunday 9am - 10am
        - "chris" teaches CMSC303 on mondays from 9am - 11am
        - **NOTE**: This may seem unnecessary, but it is very useful to break it down in this way once you have tutors that teach many classes, on
            different days and time, with multiple tutors teaching a class at the same time, or at different times. 
            This data structure keeps it all organized, and is used when making the excel sheet
        
    **Continuing app.py**:
    Now lets talk about the different funtions and classes
    - Classes: All classes besides Tutor are all subclasses of FlaskForm, they decide the interactive parts of the HTML Pages
        to learn more about them please see the offial FlaskForm documentation
    - login_manager utilizes flask_login as its login system, please see official documentation to learn more
    - Delete, insert, update, and select pages all correspond to a specific html page. They take in input from the user, and 
        do with it what the name implies... Intert_tutor adds a new tutor, delete_tutor delets a tutor
    - helper functions and routes are aditional functions that are used:
        - reset() resets the data and loads a backup into deletedData.txt
        - getUsers() grabs a set of all the valid usernames
        - createTable() calls other functions to download oldData.txt and both schedules
        - automatic_insert_old_data() runs insert_oldData() when a user logs in
        - insert_oldData() looks for oldData.txt, grabs its contents, parses it, and loads it into the three data structures
        - updateParsedData() creates the parsedData data structure from the tutors dictionary
        - downloadExistingData() demulitplexes the tutors dictionary into a CSV style string that uses ';' instead of commas
            and downloads the string into oldData.txt (or deletedData.txt if reset() is run)
        - downloadDoc() parses all_courses and put it into a microsoft word document
        - downloadExcel parses parsedData and puts it into a microsoft excel sheet
        - combineDays(set) takes a set of (day, time) pairs to make it more readable
            {(monday, 13),(monday, 14),(tuesday, 9)} turns to... Monday 1pm-3pm ... Tuesday 9am-10am
            this uses combineTimes(set) to do this
        - combineTimes(set) takes a set of times and turns them into a readable range
            (13,14,15) turns into 1pm-4pm
        - convertToRegTime(time) takes a military time and turns it into 12 hours time
            13 turns to 1pm
        - generate_random_color() returns a random color in 8 digit hex
        - day_to_num(str) returns what day of the week a certain day is, used to sort availabilites by day
        - sort_availabilities(set) takes a set of availabilites (which is a set of (day,time) tuples) and sorts them.
            They are first sorted by day, then by time
        - sort_courses(set) takes a set of courses and sorts them by subject in the order of "course_order" (please see the function)
        - update_all_courses() updates the all_courses data structure
            - when a person adds a new availability or a new course, this must be run so that all_courses can be updated. 
            - for example if Ted works BIOL101 and works on sunday 1-2, then he decides he wants to work BIOL102 as well, 
                then we must add 1-2 for BIOL102 in all_courses
            - if no name is passed, we create a new all_tutors from the tutors list, mainly used when deleting a tutor
        - sort_time_ranges(set) this takes a set of readable time ranges (such as ("1pm - 2pm", "3pm - 4pm", "9am - 10am"))
            and it sorts them to ("9am - 10am", "1pm - 2pm", "3pm - 4pm")


## Migrate Online?

If there is a want or need to put this on a server with no database, utilizing the same 3 data structures:
    - The deliverables would need to downloaded on the local machine rather than the server it is residing on
        - a copy of oldData.txt should still stay there, but the schedules do not need to be stored there
    - A system to add and delete users should be created
    - logout() should be created

If a database were to be used to store the data instead
    - The deliverables would need to downloaded on the local machine rather than the server it is residing on
        - a copy of oldData.txt should still stay there, but the schedules do not need to be stored there
    - all places where a data structure is pulled from or edited would need to utilize db.py instead.
        - the "database" branch shows a previous version where this was implemented
        - most of this work is already done in the "database" branch
    - logout() should be created

## Contact
If there are **any** questions, please email the creator of this application, Noah Shields at:
**shieldsnoahm@gmail.com**

Thank you for checking it out!