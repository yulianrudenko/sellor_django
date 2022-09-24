# Generated by Django 3.2 on 2022-09-24 23:01

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('started_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('done_deal_requested', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
                ('sent_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('is_system_generated', models.BooleanField(default=False)),
                ('is_seen', models.BooleanField(default=False)),
            ],
        ),
    ]
