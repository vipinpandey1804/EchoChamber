# Generated migration for new features

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='echogame',
            name='score',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='echogame',
            name='wall_hits',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='echogame',
            name='power_ups',
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='echogame',
            name='completed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='PowerUp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('power_type', models.CharField(choices=[('speed', 'Speed Boost'), ('phase', 'Phase Shield'), ('freeze', 'Time Freeze'), ('vision', 'Echo Vision')], max_length=20)),
                ('position', models.JSONField()),
                ('collected', models.BooleanField(default=False)),
                ('spawn_time', models.IntegerField()),
                ('expire_time', models.IntegerField()),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.echogame')),
            ],
        ),
        migrations.CreateModel(
            name='Leaderboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_id', models.CharField(max_length=100)),
                ('level', models.IntegerField()),
                ('score', models.IntegerField()),
                ('completion_time', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-score', 'completion_time'],
            },
        ),
    ]
