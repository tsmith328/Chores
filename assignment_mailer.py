import smtplib
from email.mime.text import MIMEText
import datetime
import json

# Config file containing email account information
EMAIL_CONFIG = "config/email.cfg"

# Config file containting user information (email addresses)
USER_CONFIG = "config/users.cfg"

# Email addresses for anyone who could be receiving this email
emails = {}

# Login and account info for the email sender
settings = {}

# A class which takes chore assignments and generates email messages for each person. The mailer then sends these messages using SMTP.
class AssignmentMailer(object):
    # Initializes the class with chore assignments and people
    def __init__(self, _chores, _areas, _trash_days):
        # Loads email account information before doing anything
        config_email()
        get_emails()
        self.people = _chores.keys()
        self.areas = _areas.keys()
        self.assignments = _chores
        self.descriptions = _areas
        self.trash_days = _trash_days
    
    # Sends an email to each person who has been assigned a chore. This is called after the class is initialized
    def send(self):
        for person in self.people:
            name = person
            area = self.assignments[person]
            chores = self.descriptions[area]
            trash_day = self.trash_days[name]
            body = """Hi, %s!\n\nYou have been assigned to clean %s this week. This means you should:\n\n\t-%s\n\nPlease complete these chores between Thursday afternoon and Sunday night.\n\nAnd don't forget to check the trash on %s!""" % (name, area, "\n\t-".join(chores), trash_day)
            today = datetime.datetime.today()
            subject = "Chores for the 1064 Whores [%s/%s]" % (today.month, today.day)
            send_email(emails[name], subject, body)

# Sends an email using GMail's SMTP server
def send_email(recipient, subject, body):
    # Can't send to no one!
    if len(recipient) == 0:
        return
    # Prepare the message
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = settings["name"]
    msg["To"] = recipient
    msg = msg.as_string()

    # Send!
    server = smtplib.SMTP(settings["server"], settings["port"])
    server.ehlo()
    server.starttls()
    server.login(settings["username"], settings["password"])
    server.sendmail(settings["username"], [recipient], msg)
    server.close()

# Loads email configuration information specified in EMAIL_CONFIG
# Adds settings to settings dictionary
def config_email():
    f = open(EMAIL_CONFIG, "r")

    # Populates settings dictionary with provided settings
    try:
        setting = json.load(f)
        settings["username"] = setting["username"]
        settings["password"] = setting["password"]
        settings["name"] = setting["account_name"]
        settings["server"] = setting["smtp_server"]
        settings["port"] = setting["smtp_port"]
    except:
        print("Please check the README file for the correct settings format.")
        f.close()
        exit()
    finally:
        f.close()

# Loads email addresses specified in USER_CONFIG
# Adds addresses to emails dictionary
def get_emails():
    f = open(USER_CONFIG, "r")

    # Populates address dictionary with provided addresses
    try:
        users = json.load(f)
        for key in users.keys():
            emails[key] = users[key]["email"]
    except:
        print("Please check the README file for the correct user format.")
        f.close()
        exit()
    finally:
        f.close()