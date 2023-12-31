from users import models
from rest_framework.exceptions import ValidationError

def is_client(request):
    try:
        user = models.CustomUser.objects.get(pk=request.user.pk)
        if user.is_client:
            return True
        else:
            return False
    except models.Client.DoesNotExist:
        raise ValidationError({'Error' : 'User Not Found'})
    
def object_is_exist(pk, model, exception="object not found"):
    try:
        return model.objects.get(pk=pk)
    except model.DoesNotExist:
        raise ValidationError({'Error' : f'{exception}'})