from django.db import models
from subscribes.models import SubscribeContract
from users.models import Lawyer
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Organization(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, default='Big Lawyer', unique=True)
    user = models.OneToOneField(Lawyer, on_delete=models.CASCADE, null=False, blank=False)
    subscribe_contract = models.ForeignKey(SubscribeContract, on_delete=models.CASCADE, null=False, blank=False)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=16, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)


class PaymentMethod(models.Model):
    currency_choices = (('USD', 'United States dollar'), ('EUR', 'the Euro'), ('EGP', 'Egyptian pound'))
    name = models.CharField(blank=True, null=True, max_length=255)
    account_number = models.CharField(blank=True, null=True, max_length=255)
    bank_name = models.CharField(blank=True, null=True, max_length=255)
    swift_number = models.CharField(blank=True, null=True, max_length=255)
    currency = models.CharField(choices=currency_choices, max_length = 10)
    discription = models.TextField(blank=True, null=True)


class ObjectOwnership(models.Model):
    organization   = models.ForeignKey(Organization, on_delete=models.CASCADE)
    object_id      = models.PositiveIntegerField()
    content_type   = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey('content_type', 'object_id')

