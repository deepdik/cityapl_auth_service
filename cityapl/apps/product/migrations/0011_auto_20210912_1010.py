# Generated by Django 3.2.4 on 2021-09-12 10:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_auto_20210912_0913'),
    ]

    operations = [
        migrations.AddField(
            model_name='attribute',
            name='vertical',
            field=models.ManyToManyField(through='product.AttributeInVertical', to='product.Vertical'),
        ),
        migrations.AddField(
            model_name='brand',
            name='vertical',
            field=models.ManyToManyField(through='product.BrandInVertical', to='product.Vertical'),
        ),
        migrations.AddField(
            model_name='brandinvertical',
            name='brand',
            field=models.ForeignKey(db_column='brandId', default=1, on_delete=django.db.models.deletion.CASCADE, to='product.brand'),
            preserve_default=False,
        ),
    ]
