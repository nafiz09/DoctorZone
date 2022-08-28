from email.message import EmailMessage
import ssl
import smtplib
from patient.models import *

def send_email(appointment):
    email_sender = 'abrar.cse17.buet@gmail.com'
    email_password = 'vtegsddhttsalowy'

    email_receiver = Patient.objects.get(id=appointment.patient_id).email
    #email_receiver = 'rigewi1587@ulforex.com'
    subject = 'Appointment in Dockzone'

    patient_name = Patient.objects.get(id=appointment.patient_id).first_name
    doctor_name = appointment.chamber.doctor.first_name + " " + appointment.chamber.doctor.last_name
    chamber_address = appointment.chamber.address
    date = str(appointment.date)
    otp=str(appointment.otp)

    body =f"""
    Dear {patient_name},
    Your have an appointment with Dr. {doctor_name} at his {chamber_address} Chamber on {date}.
    Your OTP is {otp}. Please let the doctor know this otp to start the appointment.
    
    Dockzone Team
    """

    print(body)

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())


