import os
import yagmail
from dotenv import load_dotenv
load_dotenv()

to = "yarndev.barclays@gmail.com"
subject = 'This is obviously the subject'
body = 'This is obviously the body'

yag = yagmail.SMTP(os.environ["EMAIL_USERNAME"], os.environ["EMAIL_APP_PASSWORD"])
yag.send(to = to, subject = subject, contents = body)