from django.core.mail import send_mail


def email_message(message_dict):
    contents = f"""
   Welcome to our bank. Here is your sign up token: {message_dict['token']}
   """
    send_mail(
        'Password Reset Token',
        contents,
        'zuz.korinkova@gmail.com',
        [message_dict['email']],
        fail_silently=False
    )
