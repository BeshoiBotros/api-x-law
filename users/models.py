from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15)
    is_client = models.BooleanField(default=False)
    is_lawyer = models.BooleanField(default=False)
    class Meta:
        verbose_name = 'CustomUser'
        
    def __str__(self):
        return self.username
    

class Client(CustomUser):

    class Meta:
        verbose_name = 'ClientUser'

    def save(self, *args, **kwargs):
        self.is_client = True
        self.is_lawyer = False
        if not self.pk or not self.password:
            self.set_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return super().username



class Lawyer(CustomUser):
    
    class Meta:
        verbose_name = "LawyerUser"

    def save(self, *args, **kwargs):
        self.is_client = False
        self.is_lawyer = True
        if not self.pk or not self.password:
            self.set_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return super().username

class LawyerProfile(models.Model):
    lawyer = models.ForeignKey(Lawyer, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profiles/', blank=True, null=True)

