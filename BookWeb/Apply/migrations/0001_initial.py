# Generated by Django 4.2.5 on 2024-10-31 02:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Groups', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('applicant', models.CharField(max_length=32, verbose_name='name')),
                ('applyreason', models.CharField(max_length=32, verbose_name='reason')),
                ('applymaxim', models.CharField(blank=True, max_length=30, verbose_name='宣言')),
                ('goal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goal_groups', to='Groups.village')),
            ],
        ),
    ]