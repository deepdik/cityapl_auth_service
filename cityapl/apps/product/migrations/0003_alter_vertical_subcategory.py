# Generated by Django 3.2.4 on 2021-06-27 13:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_rename_subcategoryname_subcategory_subcategoryname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vertical',
            name='subCategory',
            field=models.ForeignKey(db_column='subCategoryId', on_delete=django.db.models.deletion.CASCADE, to='product.subcategory'),
        ),
    ]
