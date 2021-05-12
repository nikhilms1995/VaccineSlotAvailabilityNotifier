import requests
import json
from datetime import date,timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


currentDateTime = date.today() + timedelta(days=5)
Odate = currentDateTime.strftime("%d")+"-"+currentDateTime.strftime("%m")+"-"+currentDateTime.strftime("%Y") #Needs to be in the format DD-MM-YYYY
OdistrictCode = "266"  #Find your district code based on the state code from the Cowin GetDistrictCode API 
slotAvailability = False

##Send email
senderAddress = "" #From E-mail address
senderPassword = "" #Password
receiverAddress = "" #To E-mail address
#Setup the MIME
message = MIMEMultipart()
message['From'] = senderAddress
message['To'] = receiverAddress
message['Subject'] = 'ATTENTION: Vaccination Slot Available!'   #The subject line
#The body and the attachments for the mail
mailBody = "Hello, Slots have opened up for the 18+ age category in your district.\n"
response = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id="+OdistrictCode+"&date="+Odate,
headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}) #Do not modify the headers
sessionsDictionary = json.loads(json.dumps(response.json()))
sessionCount = (len(sessionsDictionary["centers"]))
for i in range(len(sessionsDictionary["centers"])):
    for j in range(len(sessionsDictionary["centers"][i]["sessions"])):
        if sessionsDictionary["centers"][i]["sessions"][j]["min_age_limit"] == 18 and sessionsDictionary["centers"][i]["sessions"][j]["available_capacity"] > 0:
            mailBody = mailBody +"\n"+ sessionsDictionary["centers"][i]["name"]+ '\n' + "Available Count : " + str(sessionsDictionary["centers"][i]["sessions"][j]["available_capacity"]) + '\n\n'
            slotAvailability = True


if slotAvailability == True:
    #Create SMTP session for sending the mail
    message.attach(MIMEText(mailBody, 'plain'))
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(senderAddress, senderPassword) #login with e-mail and password
    text = message.as_string()
    session.sendmail(senderAddress, receiverAddress, text)
    session.quit()
    print('Slots available. E-mail has been sent with the details.')
else:
    print('Sorry! No slots available at the moment.')
    
