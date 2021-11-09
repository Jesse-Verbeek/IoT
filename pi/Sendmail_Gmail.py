import smtplib


gmail_user = 'moffel.piertje420@gmail.com'
gmail_password = 'Welkom01!'


sent_from = 'Karbonkel@student.hu.nl'
to = ['mauro.bijvank@student.hu.nl']
subject = 'Karbonkel ziet dat jij de verkeerde RFID-tag gebruikt!'
body = "Karbonkel steelt je schoenen vannacht!!\n\n- Karbonkel"

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, email_text)
    server.close()

    print( 'Email sent!')
except:
    print( 'Something went wrong...')