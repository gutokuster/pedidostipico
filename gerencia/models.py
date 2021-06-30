from django.db import models


class Configuracoes(models.Model):
    taxa_atualizacao = models.IntegerField('Taxa de atualização automática')
    data_atualizacao = models.DateTimeField('Data de Atualização', auto_now=True)

    class Meta:
        verbose_name = 'Configuração'
        verbose_name_plural = 'Configurações'