import os
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from dotenv import load_dotenv

load_dotenv()

class EmailUtility:
    @staticmethod
    def send_verification_email(user, activation_link):
        """
        Send an email to verify the user's account.
        """
        subject = 'Email Verification Required'
        sender_email = os.getenv('EMAIL_HOST_USER')
        recipient_list = [user.email]

        plain_message = f"Welcome to Videoflix! Please verify your email by clicking the link: {activation_link}"
        html_message = render_to_string('registration_email.html', {'confirmation_link': activation_link})

        message = EmailMultiAlternatives(subject, plain_message, sender_email, recipient_list)
        message.attach_alternative(html_message, "text/html")
        message.send()

    @staticmethod
    def send_password_reset_email(user, reset_link):
        """
        Send an email to reset the user's password.
        """
        subject = 'Password Reset Request'
        sender_email = os.getenv('EMAIL_HOST_USER')
        recipient_list = [user.email]

        plain_message = ("We received a request to reset your password. "
                         f"If you made this request, please use the link below to reset your password: {reset_link}")
        html_message = render_to_string('reset_password_email.html', {'reset_link': reset_link})

        message = EmailMultiAlternatives(subject, plain_message, sender_email, recipient_list)
        message.attach_alternative(html_message, "text/html")
        message.send()