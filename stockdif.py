#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
#from dotenv import load_dotenv
import os
import smtplib, ssl
## email.mime subclasses
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import pandas as pd

# Define a function to attach files as MIMEApplication to the email
##############################################################
def attach_file_to_email(email_message, filename, extra_headers=None):
    # Open the attachment file for reading in binary mode, and make it a MIMEApplication class
    with open(filename, "rb") as f:
        file_attachment = MIMEApplication(f.read())
    # Add header/name to the attachments    
    file_attachment.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )
      # Set up the input extra_headers for img
      ## Default is None: since for regular file attachments, it's not needed
      ## When given a value: the following code will run
         ### Used to set the cid for image
    if extra_headers is not None:
        for name, value in extra_headers.items():
            file_attachment.add_header(name, value)

    # Attach the file to the message
    email_message.attach(file_attachment)

def runDif():

    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    #driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
    ser = Service(os.environ.get("CHROMEDRIVER_PATH"))
    driver = webdriver.Chrome(service=ser, options=chrome_options)

    driver.get("https://bullsheet.me/auth/login")
    #driver.fullscreen_window()

    #load_dotenv()

    search = driver.find_element("xpath", '//*[@id="root"]/div/div/div[3]/div[1]/div[2]/form/div/div[2]/div/input')
    #search.send_keys(os.environ.get("bulluser"))
    search.send_keys("bulluser")

    search = driver.find_element("xpath", '//*[@id="root"]/div/div/div[3]/div[1]/div[2]/form/div/div[3]/div/input')
    #search.send_keys(os.environ.get("bullpwd"))
    search.send_keys("bullpwd")


    # click login button
    search = driver.find_element("xpath", '//*[@id="root"]/div/div/div[3]/div[1]/div[2]/form/div/div[4]/button/span')
    search.click()

    driver.implicitly_wait(500)

    # enter etoro id
    search = driver.find_element("xpath", '//*[@id="root"]/div/div/div[2]/div/div/div/div[2]/div/div/div/input')
    #search.send_keys(os.environ.get("etoro_id"))
    search.send_keys("etoro_id")
    search = driver.find_element("xpath", '//*[@id="root"]/div/div/div[2]/div/div/div/div[2]/button')
    search.click()

    # click extended hours button
    search = driver.find_element("xpath", '//*[@id="root"]/div[2]/div[1]/div/div/ul/a[3]')
    search.click()

    #body = driver.find_element("css", 'body')
    #body.send_keys(Keys.PAGE_DOWN)

    # Define the HTML document
    html = '''
        <html>
            <body>
                <h1>Daily Stock Difference Prices Report</h1>
                <p>Hello, welcome to your report!</p>
                <img src='cid:myimageid' width="700">
            </body>
        </html>
        '''

    #email_from = os.environ.get("yahoo_email")
    #passcode = os.environ.get("yahoo_passcode")
    #email_to = os.environ.get("yahoo_email")

    # Generate today's date to be included in the email Subject
    date_str = pd.Timestamp.today().strftime('%Y-%m-%d')

    # Create a MIMEMultipart class, and set up the From, To, Subject fields
    email_message = MIMEMultipart()
    email_message['From'] = yahoo_email
    email_message['To'] = yahoo_email
    email_message['Subject'] = f'Report email - {date_str}'

    # Attach the html doc defined earlier, as a MIMEText html content type to the MIME message
    email_message.attach(MIMEText(html, "html"))
    # Convert it as a string
    email_string = email_message.as_string()

    if os.path.exists("./images/*.png"):
        os.remove("./images/*.*")

    driver.get_screenshot_as_file("./images/" + date_str + "_screenshot.png")
    #driver.implicitly_wait(2000)

    # Attach more (documents)
    attach_file_to_email(email_message, "./images/" + date_str + "_screenshot.png", {'Content-ID': '<myimageid>'})

    # Convert it as a string
    email_string = email_message.as_string()

    # Connect to the Gmail SMTP server and Send Email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.mail.yahoo.com", 465, context=context) as server:
        server.login(yahoo_email, yahoo_passcode)
        server.sendmail(yahoo_email, yahoo_email, email_string)

    driver.quit()

if __name__ == "__main__":
    runDif()

