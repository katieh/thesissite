from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserForm
from django.contrib.auth.models import User, Group


# Create your views here.

## modified from example at:
## http://stackoverflow.com/questions/11287485/taking-user-input-to-create-users-in-django
def create_account(request):

	if request.method == "POST":
		form = UserForm(request.POST)

		if form.is_valid():

			## create user from form
			user = User.objects.create_user(**form.cleaned_data)

			## login
			login(request, user)

			## handle new athlete
			if request.POST['radio'] == "athlete":

				## get the athlete group
				group, created = Group.objects.get_or_create(name='athlete')
				user.groups.add(group)

				## redirect to athlete index
				return redirect('accounts:home')

			## handle new coach
			else:

				## get the coach group
				group, created = Group.objects.get_or_create(name='coach')
				user.groups.add(group)

				## redirect to coach index
				return redirect('accounts:home')



		## TODO: this should be more informative... tell them the
		## login didn't work and why.
		else:
			print "not valid"

	else:
		form = UserForm()


	return render(request, 'accounts/create.html', {'form': form})

def home(request):

	# redirect to athlete index
	if request.user.groups.filter(name='athlete'):
		return redirect('athletes:index')

	# redirect to coach index
	if request.user.groups.filter(name='coach'):
		return redirect('coaches:index')

	# THIS SHOULD NEVER RUN
	# MOSTLY FOR FIXING MIGRATION
	else:
		## get the athlete group
		group, created = Group.objects.get_or_create(name='athlete')
		request.user.groups.add(group)
		return redirect('athletes:index')
