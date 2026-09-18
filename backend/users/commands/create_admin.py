import os

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Cria ou atualiza o usuário administrador usando variáveis de ambiente."

    def handle(self, *args, **options):
        User = get_user_model()

        email = os.environ.get("ADMIN_EMAIL")
        password = os.environ.get("ADMIN_PASSWORD")
        username = os.environ.get("ADMIN_USERNAME")
        nome = os.environ.get("ADMIN_NOME", "Administrador")

        if not email:
            self.stdout.write(
                self.style.ERROR("ADMIN_EMAIL não foi definida.")
            )
            return

        if not password:
            self.stdout.write(
                self.style.ERROR("ADMIN_PASSWORD não foi definida.")
            )
            return

        if not username:
            self.stdout.write(
                self.style.ERROR("ADMIN_USERNAME não foi definida.")
            )
            return

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "username": username,
                "nome": nome,
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
            },
        )

        user.username = username
        user.nome = nome
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Administrador criado com sucesso: {email}"
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Administrador atualizado com sucesso: {email}"
                )
            )