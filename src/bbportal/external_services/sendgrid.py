import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content, TrackingSettings, ClickTracking


class BBSendgrid():
  
  @staticmethod
  def send(email,subject,content):
    sgcl = sendgrid.SendGridAPIClient(api_key=os.environ["SENDGRID_API_KEY"]).client
    mail = Mail(Email("info@insilica.co"), To(email), subject, Content("text/html", content))

    tracking_settings = TrackingSettings()
    tracking_settings.click_tracking = ClickTracking(enable=False, enable_text=False)
    mail.tracking_settings = tracking_settings
    
    return sgcl.mail.send.post(request_body=mail.get())