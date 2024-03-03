# Generated by Django 5.0.1 on 2024-03-03 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rememberApp', '0002_mytransaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='mytransaction',
            name='status',
            field=models.CharField(choices=[('waiting', 'Waiting'), ('paid', 'Paid'), ('canceled', 'Cancel')], default='waiting', max_length=600),
            preserve_default=False,
        ),
    ]