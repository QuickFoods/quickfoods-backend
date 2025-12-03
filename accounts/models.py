from django.db import models

from django.db import models
from django.contrib.auth.models import User
import uuid

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    barcode = models.CharField(max_length=20, unique=True)
    points = models.IntegerField(default=0)
    store_id = models.CharField(max_length=20, default="")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(
            user=instance,
            barcode=str(uuid.uuid4().int)[:12]  # 12-digit barcode
        )

