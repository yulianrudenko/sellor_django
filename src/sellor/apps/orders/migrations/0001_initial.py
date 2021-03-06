# Generated by Django 4.0.5 on 2022-07-22 23:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shipping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('same day delivery', 'Same day delivery'), ('overnight delivery', 'Overnight delivery'), ('regular delivery', 'Regular delivery'), ('slow delivery', 'Slow delivery')], max_length=50, unique=True, verbose_name='shipping type')),
                ('description', models.CharField(max_length=150, verbose_name='shipping type description')),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('is_completed', models.BooleanField(default=False)),
                ('shipping', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='orders.shipping')),
            ],
        ),
    ]
