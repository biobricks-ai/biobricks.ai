import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content


class BBSendgrid():
  
  @staticmethod
  def send(email,subject,content):
    key  = os.environ["SENDGRID_API_KEY"]
    sgcl = sendgrid.SendGridAPIClient(api_key=key).client
    mail = Mail(Email("info@insilica.co"), To(email), subject, Content("text/html", content)).get()
    return sgcl.mail.send.post(request_body=mail)