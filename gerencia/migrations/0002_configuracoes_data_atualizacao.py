# Generated by Django 3.2.4 on 2021-06-15 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerencia', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuracoes',
            name='data_atualizacao',
            field=models.DateTimeField(auto_now=True, verbose_name='Data de Atualização'),
        ),
    ]
