# Generated by Django 3.2.8 on 2021-10-21 21:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sitio', '0008_notification_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='canje',
            name='notification',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='sitio.notification'),
        ),
    ]