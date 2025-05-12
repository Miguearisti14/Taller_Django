from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Set roles for users'

    def handle(self, *args, **cmd_options):
      roles = {
         'Administrador': [
            'add_destinos',
            'change_destinos',
            'delete_destinos',
            'view_destinos',
            'add_comentario',
            'view_comentario'
          ],
         'Editor': [
            'add_destinos',
            'change_destinos',
            'delete_destinos',
            'view_destinos',
            'add_comentario',
            'view_comentario'
          ],
         'Usuario': [
            'view_destinos',
            'view_comentario',
            'add_comentario'
          ],
      }

      for role_name, permissions in roles.items():
        group, _ = Group.objects.get_or_create(name=role_name)
        group.permissions.clear()
        for permission in permissions:
            try:
                permissionDb = Permission.objects.get(
                  codename=permission,
                  content_type__app_label='GoTravel'
                )

                group.permissions.add(permissionDb)
            except Permission.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"Permission {permission} does not exist"))

        self.stdout.write(self.style.SUCCESS(f"Roles set for {role_name}"))