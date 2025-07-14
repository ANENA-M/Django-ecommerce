# signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import orderdItem

@receiver(post_save, sender=orderdItem)
def update_order_total_on_save(sender, instance, **kwargs):
    instance.owner.update_total()

@receiver(post_delete, sender=orderdItem)
def update_order_total_on_delete(sender, instance, **kwargs):
    instance.owner.update_total()
