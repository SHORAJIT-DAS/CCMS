import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
# To send SMS, we can use the Twilio library
# pip install twilio
from twilio.rest import Client

class EventNotificationSystem:
    def __init__(self):
        # Email configurations
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = os.environ.get("SENDER_EMAIL", "your_email@gmail.com")
        self.sender_password = os.environ.get("SENDER_PASSWORD", "your_app_password")
        
        # Twilio configurations for SMS
        self.twilio_account_sid = os.environ.get("TWILIO_ACCOUNT_SID", "your_account_sid")
        self.twilio_auth_token = os.environ.get("TWILIO_AUTH_TOKEN", "your_auth_token")
        self.twilio_phone_number = os.environ.get("TWILIO_PHONE_NUMBER", "+1234567890")
        
        try:
            self.twilio_client = Client(self.twilio_account_sid, self.twilio_auth_token)
        except Exception as e:
            self.twilio_client = None
            print(f"Twilio client not initialized: {e}")

    def send_email(self, recipient_email, recipient_name, event_details):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = f"Registration Confirmed: {event_details['eventName']}"

            body = f"""
            Hello {recipient_name},

            Your registration for the following event has been confirmed!

            Event: {event_details['eventName']}
            Club: {event_details.get('clubName', 'CCMS')}
            Date: {event_details.get('date', 'TBA')}
            Time: {event_details.get('time', 'TBA')}
            Venue: {event_details.get('venue', 'TBA')}

            Please keep your Pass ID handy: {event_details.get('regId', 'N/A')}

            Best regards,
            CCMS 2026 Team
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Setup the server
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
            server.quit()
            
            print(f"Email successfully sent to {recipient_email}")
            return True
        except Exception as e:
            print(f"Failed to send email to {recipient_email}: {e}")
            return False

    def send_sms(self, recipient_phone, recipient_name, event_details):
        if not self.twilio_client:
            print("SMS cannot be sent because Twilio client is not configured.")
            return False
            
        try:
            message_body = (
                f"Hi {recipient_name}, your registration for {event_details['eventName']} "
                f"is confirmed! Date: {event_details.get('date')} Time: {event_details.get('time')}. "
                f"Venue: {event_details.get('venue')}. Pass ID: {event_details.get('regId')}."
            )
            
            message = self.twilio_client.messages.create(
                body=message_body,
                from_=self.twilio_phone_number,
                to=recipient_phone
            )
            print(f"SMS successfully sent to {recipient_phone} (SID: {message.sid})")
            return True
        except Exception as e:
            print(f"Failed to send SMS to {recipient_phone}: {e}")
            return False

    def notify_user(self, user_data, event_details):
        print(f"--- Sending notifications for {user_data['studentName']} ---")
        email_sent = self.send_email(user_data['email'], user_data['studentName'], event_details)
        sms_sent = self.send_sms(user_data['phone'], user_data['studentName'], event_details)
        
        return {
            "email_success": email_sent,
            "sms_success": sms_sent
        }

# Example Usage
if __name__ == "__main__":
    system = EventNotificationSystem()
    
    # Mock data from CCMS Registration
    user = {
        "studentName": "Shorajit Das",
        "email": "shorajid.das@campus.edu",
        "phone": "+919841234567"
    }
    
    event = {
        "eventName": "Silver Jubilee Grand Gala",
        "clubName": "Aura Harmonics",
        "date": "Nov 15, 2026",
        "time": "06:00 PM - 10:30 PM",
        "venue": "Grand Open-Air Amphitheatre (Main Stage)",
        "regId": "REG-2026-1001"
    }
    
    # To test locally, you need valid credentials set in the environment
    # system.notify_user(user, event)
    print("Notification system initialized and ready to use.")