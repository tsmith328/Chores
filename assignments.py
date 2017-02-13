#!/usr/bin/env python

# Assigns chore areas to different people.
# Assumes that the number of areas is equal to the number of people.

# Written by: Tyler Smith
# tsmith328@gatech.edu
# September 2016

import datetime
import json
import os
import random

from assignment_mailer import AssignmentMailer
from chores_bot import postChores

# The residents of the house
people = []

# Where the last week's assignments are saved
archive_location = "last_week.chores"

# Where assignments are backed up
backup_dir = "backup"

# Areas of the house which need to be cleaned
areas = {}

# Each person has a day (except for trash day -- Monday) where they should take out the trash
trash_days = {}

# User configuration file
USER_CONFIG = "config/users.cfg"

# Area configuration file
AREA_CONFIG = "config/areas.cfg"

# Grabs user information from users.cfg including names, trash days
def get_users():
    f = open(USER_CONFIG, "r")

    # Populates trash day dictionary with provided days and people list with provided users
    try:
        users = json.load(f)
        for key in users.keys():
            if key not in people:
                people.append(key)
            trash_days[key] = users[key]["trash_day"]
    except:
        print("Please check the README file for the correct user format.")
        f.close()
        exit()
    finally:
        f.close()

# Grabs chore information from areas.cfg including area name and tasks
def get_areas():
    f = open(AREA_CONFIG, "r")

    # Populates areas dictionary with areas provided in areas.cfg
    try:
        area = json.load(f)
        for key in area.keys():
            areas[key] = area[key]
    except:
        print("Please check the README file for the correct area format.")
        f.close()
        exit()
    finally:
        f.close()

def generate_chores(_areas, _people):
    """Assign a random chore area to each person. Return a dictionary mapping people to areas."""
    # if len(_areas) != len(_people): # Assumes there are as many chores as people
    #     print ("There should be as many people as chore areas!")
    #     exit(-1)
    
    # Generate random chore assignments
    chores = random.sample(range(1, len(_areas) + 1), len(_people))

    assignments = {}
    # Assign chores to each person
    for i, person in enumerate(people):
        assignments[person] = "Area %d" % (chores[i])
    
    return assignments

def verify_assignments(_assignments):
    """Verify that assignments are not repeated from the previous assignments. Return True if valid, False otherwise"""
    last_week = {}

    # If previous assignments do not exist, assume these assignments are valid
    if not os.path.isfile(archive_location):
        return True

    # Read previous assignments from archive file
    with open(archive_location, "r") as f:
        for line in f:
            last_week[line.split(":")[0].strip()] = line.split(":")[1].strip()
    
    # Check that each person has a new chore
    try:
        for person in _assignments.keys():
            if _assignments[person] == last_week[person]:
                return False
    except KeyError:
        # There's a problem with the archive file. Delete it.
        os.remove(archive_location)
        return True

    # If we reach this point, all chores are new, so the assignments are valid
    return True

# Archives the assigned chores so that they can be compared to the next week's chores
def archive_chores(_assignments):
    save = "\n".join(["%s: %s" % (p, _assignments[p]) for p in _assignments.keys()])
    with open(archive_location, "w") as f:
        f.write(save)

# Backs up the currently saved previous chores for inspection later if necessary
def backup_chores():
    # Check that the backup directory exists
    if not os.path.isdir(backup_dir):
        os.mkdir(backup_dir)
    # Create the name of the backup file. YYYY-MM-DD.chores
    today = datetime.datetime.today()
    backup = "-".join([str(today.year), str(today.month), str(today.day)]) + ".chores"
    # Open the current archive to copy to the backup location
    w = open(os.path.join(backup_dir, backup), "w")
    try:
        r = open(archive_location, "r")
    except:
        # If the archive doesn't exist, just make an empty one
        open(archive_location, "w").close()
        r = open(archive_location, "r")
    # Copy copy copy
    for line in r:
        w.write(line)
    w.close()
    r.close()
    
# When called, generates assignments for chores, verifies them, then saves them to an archive file.
# Then uses assignment sender to email out assignments.
def main():
    # Get user and area info
    get_users()
    get_areas()
    # Generate assignments
    chore_assignments = generate_chores(areas, people)
    # Make sure they're not repeats
    while(not verify_assignments(chore_assignments)):
        chore_assignments = generate_chores(areas, people)
    # Backup previous assignments
    backup_chores()
    # Save these assignments
    archive_chores(chore_assignments)

    # Now we have to send the assignments to everyone
    # Use AssignmentMailer to distribute
    mailer = AssignmentMailer(chore_assignments, areas, trash_days)
    mailer.send()

    # Then, post to GroupMe
    postChores(chore_assignments)

if __name__ == "__main__":
    main()
