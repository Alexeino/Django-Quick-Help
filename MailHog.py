# Setting UP Mail Hog for Local Email Testing

## Mailhog Windows Link : https://sourceforge.net/projects/mailhog.mirror/

# Settings.py

# SMTP for Mailhog
EMAIL_HOST = 'localhost'
EMAIL_PORT = '1025'

# Sending Emails

from django.core.mail import send_mail
# Sending email with custom token for validation

send_mail(
  subject="Reset Your Password!",
  message='Click <a href="%s">here</a> to Reset Password '%url,
  from_email='admin@example.com',
  recipient_list=[email]
        )
