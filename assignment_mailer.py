import smtplib
from email.mime.text import MIMEText
import datetime

# Email addresses for anyone who could be receiving this email. This should be the residents of the house
emails = {"Tyler": "t.m.s015@gmail.com",
          "Banjo": "krabagobanjo@outlook.com",
          "Laura": "llhudd3@gmail.com",
          "Jessica": "jessicabritt@gatech.edu",
          "Emily": "emilykiehn@gmail.com",
          "Haley": "haleyalexish@gmail.com"}

# Login and account info for the email sender
email_user = "1064chores@gmail.com"
email_password = "1064Atlantic"
mail_name = "Chore Assignments"
smtp_server = "smtp.gmail.com"
smtp_port = 587

# A class which takes chore assignments and generates email messages for each person. The mailer then sends these messages using SMTP.
class AssignmentMailer(object):
    # Initializes the class with chore assignments and people
    def __init__(self, _chores, _areas, _trash_days):
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
    msg["From"] = mail_name
    msg["To"] = recipient
    msg = msg.as_string()

    # Send!
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.ehlo()
    server.starttls()
    server.login(email_user, email_password)
    server.sendmail(email_user, [recipient], msg)
    server.close()