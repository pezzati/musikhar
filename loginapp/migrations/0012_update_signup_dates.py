from django.db import migrations


def update_signup_dates(apps, schema_editor):
    Users = apps.get_model('loginapp', 'User')

    db_alias = schema_editor.connection.alias

    users, counter = Users.objects.using(db_alias).all(), 0

    for user in users:
        if not user.is_guest:
            user.signup_date = user.date_joined
            user.save()
            counter += 1

            print('{}- user: {} signup_date updated'.format(counter, user.id))


def reverse_signup_dates(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('loginapp', '0011_user_signup_date'),
    ]

    operations = [
        migrations.RunPython(update_signup_dates, reverse_signup_dates)

    ]
