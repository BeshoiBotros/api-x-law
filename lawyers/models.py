from django.db import models
from users.models import CustomUser

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
