from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from api_yamdb.settings import DEFAULT_FROM_EMAIL


def send_confirmation_code(user):
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Код подтверждения',
        message=f'Ваш одноразовый код подтверждения: "{confirmation_code}".',
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=True,
    )
