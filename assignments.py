# Assigns chore areas to different people.
# Assumes that the number of areas is equal to the number of people.

# Written by: Tyler Smith
# tsmith328@gatech.edu
# September 2016

import random
import os
from assignment_mailer import AssignmentMailer

# The residents of the house
people = ["Tyler", "Banjo", "Jessica", "Emily", "Laura", "Haley"]

# Where the last week's assignments are saved
archive_location = "./last_week.chores"

# Where assignments are backed up
backup_dir = "./backup/"

# Areas of the house which need to be cleaned
areas = {"Area 1" : ["Sweep and mop the kitchen floor", "Sweep and mop the front bathroom floor"],
         "Area 2" : ["Sweep and mop the study floor", "Sweep and mop the back bathroom floor"],
         "Area 3" : ["Sweep and mop the laundry room floor", "Wipe down the washer and dryer", "Wipe down the dining table"],
         "Area 4" : ["Clean the kitchen counters", "Clean the kitchen sink", "Clean the insides and tops of appliances"],
         "Area 5" : ["Sweep and swiffer the living room floor", "Vacuum the couches and futon"],
         "Area 6" : ["Clean and dust all windows and blinds downstairs (including bathrooms)", "Dust the electronics", "Move the trash cans to the street on Sunday night"]}

# Each person has a day (except for trash day -- Monday) where they should take out the trash
trash_days = {"Tyler" : "Sunday",
              "Banjo" : "Thursday",
              "Laura" : "Wednesday",
              "Haley" : "Tuesday",
              "Emily" : "Saturday",
              "Jessica" : "Friday"}

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

    
# When called, generates assignments for chores, verifies them, then saves them to an archive file.
# Then uses assignment sender to email out assignments.
def main():
    # Generate assignments
    chore_assignments = generate_chores(areas, people)
    # Make sure they're not repeats
    while(not verify_assignments(chore_assignments)):
        chore_assignments = generate_chores(areas, people)
    # Save these assignments
    archive_chores(chore_assignments)

    # Now we have to send the assignments to everyone
    # Use AssignmentMailer to distribute
    mailer = AssignmentMailer(chore_assignments, areas, trash_days)
    mailer.send()

if __name__ == "__main__":
    main()