# Generated by Django 4.2.13 on 2024-06-22 07:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['first_name', 'last_name']},
        ),
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['-id', 'title', 'author']},
        ),
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': (('can_marked_return', 'Set Book Renew Due-Date'),)},
        ),
    ]
