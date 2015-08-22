#!/usr/bin/python
# -*- coding: utf-8 -*-
from instagram.client import InstagramAPI
from instagram.bind import InstagramAPIError
from pprint import pprint
from urllib2 import Request, urlopen, URLError, HTTPError
from time import sleep
def DownloadImage(filename,base_url):
	sleep(2)
	url = base_url 
	req = Request(url)
	ext = base_url.rpartition('.')[-1]
	# Open the url
	jpg = filename +'.'+ ext
	try:
		f = urlopen(req)
		print "downloading " + url
		
		# Open our local file for writing
		local_file = open(jpg, "w")
		#Write to our local file
		local_file.write(f.read())
		local_file.close()
		
	#handle errors
	except HTTPError, e:
		print "HTTP Error:",e.code , url
		pass
	except URLError, e:
		print "URL Error:",e.reason , url
		pass
	except StandardError:
		print "URL Error:" , url
		pass
def GetMyFollowers(my_user_id, api):
	follows, next_ = api.user_follows(user_id=my_user_id)
	while next_:
		more_follows, next_ = api.user_follows(with_next_url=next_)
		follows.extend(more_follows)
		sleep(2)
		return follows
def GetMediaFromUser(following, api, photos):

	most_liked = 0
	most_liked_photo =""
	mostLikedObject=["",0,""]

	try:
		recent_media, next = api.user_recent_media(user_id=following.id)
		sleep(2)
			
	except InstagramAPIError as e:
		if (e.status_code == 400):
			print "\nUser is set to private."
	except AttributeError:
		print "There's no attribute for that id"
		#traceback.print_exc()
		pass

	while next:
		try:
			more_media, next = api.user_recent_media(with_next_url=next)
			recent_media.extend(more_media)
			sleep(2)
		except InstagramAPIError as e:
			if (e.status_code == 400):
				print "\nUser is set to private."
				pass
		except AttributeError:
			print "There's no attribute for that id"
			#traceback.print_exc()
			pass
		for media in recent_media:
			mostLikedObject[0]=media.user.username
			if(media.like_count > most_liked):
				most_liked = media.like_count
				most_liked_photo= media.images['standard_resolution'].url
				mostLikedObject[1]=most_liked
				mostLikedObject[2]=most_liked_photo

	if(mostLikedObject[1]!=0):
		photos.append(mostLikedObject)
		DownloadImage( (mostLikedObject[0]+ '__'+str(mostLikedObject[1])), mostLikedObject[2])
	for allmostliked in photos:
		print allmostliked
	
def main():
	#ADD YOUR CLIENT ID AND SECRET
	my_client_id=''
	my_client_secret=''
	#ADD A USER ID WITH FOLLOWERS 
	my_user_id=""
	
	api = InstagramAPI(client_id=my_client_id, client_secret=my_client_secret)

	pprint(vars(api))
	
	
	my_followers=GetMyFollowers(my_user_id,api)
	
	photos = []

	for following in my_followers:
		GetMediaFromUser(following, api, photos)
		print '************************************'



if __name__ == "__main__":
	main()	



