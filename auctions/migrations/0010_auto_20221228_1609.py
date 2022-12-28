# Generated by Django 3.0 on 2022-12-28 16:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_watchlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watchlist',
            name='item_name',
        ),
        migrations.AddField(
            model_name='watchlist',
            name='item_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='item_id', to='auctions.Listing'),
        ),
    ]