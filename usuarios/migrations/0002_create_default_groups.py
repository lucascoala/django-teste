from django.db import migrations

def create_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    groups = [
        'Reunioes', 'Celulas', 'Visitantes', 'Membros',
        'Financeiro', 'Salas', 'Matriz', 'Missao',
        'Usuarios', 'Despesas', 'Contribuicoes'
    ]
    for group_name in groups:
        Group.objects.get_or_create(name=group_name)

def delete_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_groups, delete_groups),
    ]