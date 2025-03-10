import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content


class BBSendgrid():
  
  @staticmethod
  def send(email,subject,content):
    sgcl = sendgrid.SendGridAPIClient(api_key=os.environ["SENDGRID_API_KEY"]).client
    mail = Mail(Email("info@insilica.co"), To(email), subject, Content("text/html", content))
    mail.tracking_settings = {"click_tracking": {"enable": False}}
    return sgcl.mail.send.post(request_body=mail.get())