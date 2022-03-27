from django.db.models.signals import post_save
from django.dispatch import receiver
from user.models import User
from library.mailchimp.send_mail import sendMail
import mandrill
from coutoEditor.global_variable import MANDRILL_API_KEY


@receiver(post_save, sender=User)
def post_save_prediction(sender, instance, created, **kwargs):

    if created:
        signup_template = "3 Getting started"
        name = instance.username
        subject = "Signed Up On Video-wiki"
        global_merge_vars = [
            {
                'name': 'NAME',
                'content': name,
            }

        ]
        sendMail(signup_template, instance.email, name, subject, global_merge_vars)

def send_otp_details(email, otp):
    name = email.split('@')[0]
    global_merge_vars = [
        {
            'name': 'NAME',
            'content': name,
        }

    ]
    subject = otp
    status = send_otp_mail(email, name, subject, global_merge_vars, otp)
    return status


def send_otp_mail( to_email, name,subject, global_merge_vars, otp):
    try:
        mandrill_client = mandrill.Mandrill(MANDRILL_API_KEY)
        message = {
            'from_email': 'support@videowiki.pt',
            'from_name': 'VideoWiki',
            'global_merge_vars': global_merge_vars,
            # need reply mail
            'headers': {'Reply-To': 'support@videowiki.pt'},
            'merge': True,
            'merge_language': 'mailchimp',
            'subject': "OTP",
            'tags': ['password-resets'],
            'text': str(otp),
            'to': [{'email': to_email,
                    'name': name,
                    'type': 'to'}],
        }
        result = mandrill_client.messages.send(message=message)
        print(result)
        status = result[0]['status']
        return status
    except mandrill.Error as e:
        status = 'A mandrill error occurred:'
        print('A mandrill error occurred:')
        return status

def send_reset_mail(email, url):
    name = email.split('@')[0]
    global_merge_vars = [
        {
            'name': 'NAME',
            'content': name,
        }

    ]
    subject = "Password Reset Mail"
    status = send_pass_reset_mail(email, name, subject, global_merge_vars, url)
    return status

def send_pass_reset_mail( to_email, name, subject, global_merge_vars, url):
    try:
        mandrill_client = mandrill.Mandrill(MANDRILL_API_KEY)
        message = {
            'from_email': 'support@videowiki.pt',
            'from_name': 'Video.Wiki',
            'global_merge_vars': global_merge_vars,
            # need reply mail
            'headers': {'Reply-To': 'support@videowiki.pt'},
            'merge': True,
            'merge_language': 'mailchimp',
            'subject': str(subject),
            'tags': ['password-resets'],
            'text': "{}".format(url),
            'to': [{'email': to_email,
                    'name': name,
                    'type': 'to'}],
        }
        result = mandrill_client.messages.send(message=message)
        print(result)
        status = result[0]['status']
        return status
    except mandrill.Error as e:
        status = 'A mandrill error occurred:'
        print('A mandrill error occurred:')
        return status