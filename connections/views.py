from django.contrib.auth.models import User, Group
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from friendship.models import Friend, FriendshipRequest
from friendship.exceptions import AlreadyExistsError, AlreadyFriendsError

# Create your views here.

# modified from example at: https://github.com/revsys/django-friendship
# NOTE: only an ahtlete can begin a friend request
@login_required
def add(request, pk):
	coach = get_object_or_404(User, pk=pk)

	try:
		Friend.objects.add_friend(request.user, coach)

	except (AlreadyExistsError, AlreadyFriendsError):
		print "frienship is pending or already exists"

	# redirect to previous page
	return redirect('athletes:connections')

# modified from example at: https://github.com/revsys/django-friendship
# NOTE: only coaches can accept / reject a friend request
@login_required
def confirm(request, pk):

	friend_request = FriendshipRequest.objects.get(pk=pk)
	friend_request.accept()

	return redirect('coaches:connections')


# modified from example at: https://github.com/revsys/django-friendship
# NOTE: only coaches can accept / reject a friend request
@login_required
def reject(request, pk):

	friend_request = FriendshipRequest.objects.get(pk=pk)
	friend_request.reject()

	return redirect('coaches:connections')


# modified from example at: https://github.com/revsys/django-friendship
@login_required
def unfriend(request, pk):

	other_user = User.objects.get(pk=pk)

	friend = Friend.objects.remove_friend(request.user, other_user)

	# redirect to athlete index
	if request.user.groups.filter(name='athlete'):
		return redirect('athletes:connections')

	# redirect to coach index
	if request.user.groups.filter(name='coach'):
		return redirect('coaches:connections')



