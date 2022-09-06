from django.contrib.auth.forms import UserCreationForm

from .models import User


class UserCr(UserCreationForm):
    
    class Meta:
        model = User 
        fields = ('username', )