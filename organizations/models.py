from django.db import models
from subscribes.models import SubscribeContract
from users.models import Lawyer

class Organization(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, default='Big Lawyer')
    user = models.ForeignKey(Lawyer, on_delete=models.CASCADE, null=False, blank=False)
    subscribe_contract = models.ForeignKey(SubscribeContract, on_delete=models.CASCADE, null=False, blank=False)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=16, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)


