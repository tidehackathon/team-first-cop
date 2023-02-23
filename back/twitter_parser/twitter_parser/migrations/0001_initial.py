# Generated by Django 4.1.7 on 2023-02-21 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sources',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.TextField()),
                ('enabled', models.BooleanField(default=True)),
                ('add_date', models.DateTimeField(null=True)),
            ],
            options={
                'verbose_name_plural': 'Sources',
                'db_table': 'sources',
            },
        ),
        migrations.CreateModel(
            name='TwitterSources',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.TextField(db_index=True)),
                ('has_photo', models.BooleanField(default=False)),
                ('channel_about', models.TextField(null=True)),
                ('channel_title', models.TextField(null=True)),
                ('creation_date', models.DateTimeField(null=True)),
                ('followers', models.IntegerField(null=True)),
                ('location', models.TextField(null=True)),
                ('source', models.ManyToManyField(to='twitter_parser.sources')),
            ],
            options={
                'verbose_name_plural': 'Twitter Sources',
                'db_table': 'twitter_sources',
            },
        ),
        migrations.CreateModel(
            name='TwitterMessages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tweet_id', models.TextField()),
                ('date', models.DateTimeField(null=True)),
                ('text', models.TextField(null=True)),
                ('retweet', models.IntegerField(null=True)),
                ('likes', models.IntegerField(null=True)),
                ('location', models.TextField(null=True)),
                ('has_media', models.BooleanField()),
                ('media', models.TextField(blank=True, null=True)),
                ('is_quote', models.BooleanField(blank=True, null=True)),
                ('quote_id', models.TextField(blank=True, null=True)),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='twitter_parser.twittersources')),
            ],
            options={
                'verbose_name_plural': 'Twitter Messages',
                'db_table': 'twitter_messages',
            },
        ),
    ]