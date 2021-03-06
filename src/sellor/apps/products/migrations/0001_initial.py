# Generated by Django 4.0.5 on 2022-07-22 23:21

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('clothes', 'Clothes'), ('it', 'It'), ('food', 'Food'), ('sport', 'Sport'), ('study', 'Study'), ('health', 'Health'), ('entertainment', 'Entertainment'), ('house', 'House'), ('books', 'Books'), ('service', 'Service'), ('weapons', 'Weapons')], max_length=50, unique=True, verbose_name='category name')),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='CouponCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=16, unique=True, verbose_name='coupon code')),
                ('reduce_amount', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('nike', 'Nike'), ('adidas', 'Adidas'), ('viral', 'Viral'), ('school', 'School'), ('new', 'New'), ('old', 'Old'), ('very cheap', 'Very cheap'), ('natural', 'Natural'), ('punk', 'Punk'), ('animals', 'Animals'), ('computer', 'Computer'), ('programming', 'Programming'), ('funny', 'Funny'), ('football', 'Football'), ('anime', 'Anime')], max_length=50, unique=True, verbose_name='tag name')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50, verbose_name='title')),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('discount_price', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('description', models.CharField(blank=True, max_length=300, null=True, verbose_name='description')),
                ('image', models.ImageField(default='../static/images/blank.jpg', help_text='Upload an image', upload_to='images/products', verbose_name='image')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.category')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='orders.order')),
                ('tags', models.ManyToManyField(blank=True, to='products.tag')),
            ],
        ),
    ]
