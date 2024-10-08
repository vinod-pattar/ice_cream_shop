# Generated by Django 4.2.15 on 2024-09-02 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0013_alter_cartitem_price_alter_cartitem_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='amount_due',
            field=models.FloatField(blank=True, default=0.0),
        ),
        migrations.AddField(
            model_name='order',
            name='amount_paid',
            field=models.FloatField(blank=True, default=0.0),
        ),
        migrations.AddField(
            model_name='order',
            name='currency',
            field=models.CharField(default='INR', max_length=10),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_status',
            field=models.CharField(default='pending', max_length=20),
        ),
        migrations.AddField(
            model_name='order',
            name='receipt',
            field=models.CharField(blank=True, editable=False, max_length=128, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(editable=False, max_length=128, unique=True),
        ),
    ]
