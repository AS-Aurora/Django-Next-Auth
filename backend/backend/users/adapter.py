from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

class CustomAccountAdapter(DefaultAccountAdapter):
    def send_confirmation_mail(self, request, emailconfirmation, signup):
        user = emailconfirmation.email_address.user
        activate_url = f"{settings.FRONTEND_URL}/verify-email?key={emailconfirmation.key}"

        ctx = {
            "user": user,
            "activate_url": activate_url,
            "key": emailconfirmation.key,
        }

        message = render_to_string("account/email/email_confirmation_message.txt", ctx)
        subject = render_to_string("account/email/email_confirmation_subject.txt", ctx).strip()

        email = EmailMessage(subject, message, to=[user.email])
        email.send()
