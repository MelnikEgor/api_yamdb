import uuid

from django.core.mail import send_mail

from api_yamdb.settings import DEFAULT_FROM_EMAIL


def send_confirmation_code(user):
    confirmation_code = uuid.uuid5(uuid.NAMESPACE_DNS, user.username)
    user.confirmation_code = confirmation_code
    user.save()
    send_mail(
        subject='Код подтверждения',
        message=f'Ваш код подтверждения: {confirmation_code}.',
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=True,
    )
