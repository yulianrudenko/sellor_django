# Generated by Django 3.2 on 2022-09-24 23:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('chats', '0001_initial'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(max_length=100, verbose_name='first name')),
                ('last_name', models.CharField(max_length=100, verbose_name='last name')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='phone')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('X', 'Other')], default='X', max_length=1, verbose_name='gender')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_activated', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(default='../static/images/blank.jpg', help_text='Upload an avatar', upload_to='images/profile_pics', verbose_name='image')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Cities',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(blank=True, max_length=55, null=True, unique=True)),
                ('visited_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReportUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(blank=True, max_length=200, null=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('report_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports_author', to=settings.AUTH_USER_MODEL)),
                ('reported_message', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='report', to='chats.message')),
                ('user_reported', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports_subject', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Report',
                'verbose_name_plural': 'User Reports',
            },
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=250)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('upvoted_by', models.ManyToManyField(blank=True, related_name='upvoted_posts', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='useraccount',
            name='location',
            field=models.ForeignKey(max_length=35, on_delete=django.db.models.deletion.CASCADE, to='users.city', verbose_name='location(city)'),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='wishlist',
            field=models.ManyToManyField(blank=True, related_name='wishlists', to='products.Product'),
        ),
        migrations.CreateModel(
            name='Blacklist',
            fields=[
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='blacklist', serialize=False, to='users.useraccount')),
                ('blocked_users', models.ManyToManyField(blank=True, related_name='blocked_by_others', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
