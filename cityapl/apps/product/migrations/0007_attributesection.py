# Generated by Django 3.2.4 on 2021-09-09 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_auto_20210801_0743'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttributeSection',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'attribute_section',
            },
        ),
    ]
