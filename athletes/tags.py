from .models import Tag
import requests


# modified from http://text-processing.com/docs/sentiment.html
def get_sentiment_tags(activity):

	# post to text-processing to do sentiment analysis
	r = requests.models.Response()
	while r.status_code != 200:
		r = requests.post("http://text-processing.com/api/sentiment/", data={'text': activity.comments})

	# get the probabilities associated with the comment	
	probabilities = r.json()['probability']

	# save each probability as a sentiment tag
	for key in ['neg', 'pos']:
		tag = Tag()

		# save user info
		tag.user = activity.user
		tag.run = activity

		# save tag info
		tag.tag = "sentiment_{}".format(key)
		tag.date = activity.start_time
		tag.value = probabilities[key]

		tag.save()

def get_user_tags(activity):

	# get all words in the comment
	words = activity.tags.split()
	words += activity.comments.split()

	# get the hashtags and their associated values if they exist
	for i in range(len(words)):
		print words[i]
		if words[i].startswith("#"):

			# we're going to save a new hashtag
			# with the current word
			tag = Tag()
			tag.user = activity.user
			tag.run	= activity
			tag.date = activity.start_time
			tag.tag = words[i].rstrip('?:!.,;')

			# check to see if there's an associated value; if not
			# or if we can't cast it, associate it with 1
			try:
				tag.value = float(words[i + 1])
			except:
				tag.value = 1

			try:
				previous_tag = Tag.objects.filter(user=activity.user, tag=tag.tag).latest()
				tag.allow_access = previous_tag.allow_access
			except:
				pass

			# save the tag!
			tag.save()



