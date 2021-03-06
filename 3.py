import smtplib, ssl, email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
import csv

def enviar_email(sender_mail, sender_pwd, subject, body, dst_mail, file):
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_mail
    message.attach(MIMEText(body, "plain"))
    filename = file

    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    body = message.as_string()


    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        try:
            server.login(sender_mail, sender_pwd)
            server.sendmail(
                sender_mail, dst_mail, message.as_string()
            )
        except Exception:
            print("ERROR!")
    print("OK!")
    

file = input("Introduce la ruta completa del CSV :")
with open (file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count +=1
        else:
            mail = row[0]
            attach = row[1]
            subject = row[2]
            body = row[3]
            enviar_email('miskojones98@gmail.com', '!abc123.,',subject, body, mail, attach)
            
    


