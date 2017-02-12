from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from friendship.models import FriendshipRequest, Friend
from django.contrib.auth.models import User

# coaches home view
@login_required
def index(request):
	return render(request, 'coaches/index.html', {'nbar': 'home'})

# coaches list view of athletes
def list(request):
	return render(request, 'coaches/list.html', {'nbar':'athletes'})

def connections(request):

	friendship_requests = FriendshipRequest.objects.filter(to_user_id=request.user.id)

	request_data = []

	# get information about who made the request!
	for friendship_request in friendship_requests:

		user = User.objects.get(pk=friendship_request.from_user_id)

		request_data.append({'request_id': friendship_request.id,
			'first_name': user.first_name,
			'last_name': user.last_name})

	# get information on the current friendships
	friends = Friend.objects.filter(from_user_id=request.user.id)

	friend_data = []

	for friend in friends:

		user = User.objects.get(pk=friend.to_user_id)

		friend_data.append({'friend_id': user.id,
			'first_name': user.first_name,
			'last_name':user.last_name})


	return render(request, 'coaches/connections.html', 
		{'request_data': request_data,
		'friend_data': friend_data})

