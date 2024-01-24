from django.db import models
from users.models import Lawyer

class Category(models.Model):
    name = models.CharField(max_length=255)

class New(models.Model):
    title = models.CharField(max_field=255)
    user = models.ForeignKey(Lawyer, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subject = models.TextField(blank=False, null=False)
    image = models.ImageField(upload_to='news/images/', null=True, blank=True)

class Case(models.Model):
    title = models.CharField(max_field=255)
    user = models.ForeignKey(Lawyer, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subject = models.TextField(blank=False, null=False)

