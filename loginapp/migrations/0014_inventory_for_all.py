from django.db import migrations


def create_inventory(apps, schema_editor):
    Users = apps.get_model('loginapp', 'User')
    Inventories = apps.get_model('inventory', 'Inventory')

    db_alias = schema_editor.connection.alias

    users, counter = Users.objects.using(db_alias).all(), 0

    for user in users:
        Inventories.objects.get_or_create(user=user)
        print('{}- user: inventory created'.format(user.id))


def reverse_create_inventory(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('loginapp', '0013_user_coins'),
    ]

    operations = [
        migrations.RunPython(create_inventory, reverse_create_inventory)

    ]
