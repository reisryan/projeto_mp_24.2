from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Barraca, Localizacao

@receiver(post_save, sender=User)
def criar_localizacao_usuario(sender, instance, created, **kwargs):
    if created and (instance.latitude is None or instance.longitude is None):
        localizacao = Localizacao.gerar_localizacao()
        instance.latitude = localizacao.latitude
        instance.longitude = localizacao.longitude
        instance.save()

@receiver(post_save, sender=Barraca)
def criar_localizacao_barraca(sender, instance, created, **kwargs):
    if created and (instance.latitude is None or instance.longitude is None):
        latitude, longitude = Localizacao.gerar_localizacao()
        instance.latitude = latitude
        instance.longitude = longitude
        instance.save()