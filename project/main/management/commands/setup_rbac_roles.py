from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

from main.rbac import CRUD_MODELS

User = get_user_model()

from main.models import ManagedModule

managed_model_names = ManagedModule.objects.filter(is_active=True).values_list(
    'content_type__model', flat=True
)

DEFAULT_ROLES = {
    'Admin': {m: ['view', 'add', 'change', 'delete'] for m in managed_model_names},
    'Teacher': {
        'notice': ['view', 'add', 'change', 'delete'],
    },
    'Student': {
        'notice': ['view'],
        'event': ['view'],
    },
}


class Command(BaseCommand):
    help = 'Create starter Admin/Teacher/Student roles and migrate existing staff users into Admin.'

    def handle(self, *args, **options):
        for role_name, model_actions in DEFAULT_ROLES.items():
            group, created = Group.objects.get_or_create(name=role_name)
            perms = []

            for model_name, actions in model_actions.items():
                for action in actions:
                    codename = f'{action}_{model_name}'
                    try:
                        perm = Permission.objects.get(
                            content_type__app_label='main',
                            content_type__model=model_name,
                            codename=codename,
                        )
                        perms.append(perm)
                    except Permission.DoesNotExist:
                        self.stdout.write(self.style.WARNING(
                            f'Permission "{codename}" for main.{model_name} not found. '
                            f'Run "python manage.py migrate" first.'
                        ))

            group.permissions.set(perms)
            self.stdout.write(self.style.SUCCESS(
                f'{"Created" if created else "Updated"} role "{role_name}" '
                f'with {len(perms)} permission(s).'
            ))

        admin_group = Group.objects.get(name='Admin')
        staff_users = User.objects.filter(is_staff=True, is_superuser=False)
        count = 0
        for user in staff_users:
            user.groups.add(admin_group)
            count += 1

        self.stdout.write(self.style.SUCCESS(
            f'Added {count} existing staff user(s) to "Admin". '
            f'Superusers were left as-is (they bypass permission checks).'
        ))
