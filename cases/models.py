from django.db import models
from users import models as users_models

class Category(models.Model):
    name = models.CharField(max_length=255)

class New(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(users_models.Lawyer, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subject = models.TextField(blank=False, null=False)
    image = models.ImageField(upload_to='news/images/', null=True, blank=True)

class Case(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(users_models.Lawyer, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subject = models.TextField(blank=False, null=False)

class Comment(models.Model):
    user = models.ForeignKey(users_models.CustomUser, on_delete=models.CASCADE)
    new = models.ForeignKey(New, on_delete=models.CASCADE)
    comment = models.TextField(blank=False, null=False)

class Like(models.Model):
    user = models.ForeignKey(users_models.CustomUser, on_delete=models.CASCADE)
    new = models.ForeignKey(New, on_delete=models.CASCADE)

