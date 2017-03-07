from django.contrib.auth.models import User
from django.forms import ModelForm


## modified from:
## http://stackoverflow.com/questions/11287485/taking-user-input-to-create-users-in-django

class UserForm(ModelForm):
	class Meta:
		model = User
		fields = ['username', 'password', 'first_name', 'last_name', 'email']
		