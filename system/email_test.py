import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adowes_site.settings')
django.setup()

from django.core.mail import send_mail

send_mail(
    'Teste Django Email',
    'Este é um email de teste enviado do Django.',
    'adowes4@gmail.com',  # remetente
    ['henrickypedro.barbosa@gmail.com'],  # destinatário
    fail_silently=False,
)

print('Email enviado com sucesso!')