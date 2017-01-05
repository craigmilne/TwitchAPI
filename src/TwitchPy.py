# TwitchPy

from urllib.error import HTTPError
from urllib.request import Request, urlopen  # Python 3
from urllib import urlencode

import json

# Decodes the JSON requests
def decode(data):
	def wrapper(*args):
		res = data(*args)
		if res == None:
			return None
		else:
			return json.loads(res)
	return wrapper

class TwitchPy():
	
	# Requires a client id to use
	def __init__(self, clientId, accessToken=""):
		self.cid = str(clientId)
		self.aut_tken = str(accessToken)
		self.api_root = "https://api.twitch.tv/kraken/"
		self.acc_head = "application/vnd.twitchtv.v5+json"

	@staticmethod
	def version():
		return "v0.1.0"

	# Set where we go for the API
	def setAPIRoot(self, newApi):
		self.api_root = str(newApi)

	# Set the API version to use etc
	def setAcceptHeaderField(self, newHead):
		self.acc_head = str(newHead)

	# Set the client ID
	def setClientID(self, clientId):
		self.cid = str(clientId)

	def setAuthToken(self, accessToken):
		self.aut_tken = str(accessToken)

	# Ping the API, returns the HTTP error code
	def ping(self):
		try:
			r = Request(self.api_root)
			r.add_header('Client-ID', self.cid)
			r.add_header('Accept', self.acc_head)
			a = str(urlopen(r).read()).decode("cp850")
		except HTTPError as ex:
			if ex.code == 400:
				print("Failed to authenticate. Is Client-ID correct? (HTTP/1.1 400)")
			else:
				print("An unexpected error occured: (HTTP/1.1 " + str(ex.code) + ")")
			return ex.code
		return 200

	# GET a decoded JSON from a query
	@decode
	def request(self, req):
		try:
			r = Request(self.api_root + str(req))
			r.add_header('Client-ID', self.cid)
			r.add_header('Accept', self.acc_head)
			if self.aut_tken != "":
				r.add_header('Authorization', "OAuth " + self.aut_tken)
			a = urlopen(r).read().decode("cp850")
		except HTTPError as ex:
			if ex.code == 400:
				print("Failed to authenticate. Is Client-ID correct? (HTTP/1.1 400)")
			else:
				print("An unexpected error occured: (HTTP/1.1 " + str(ex.code) + ")")
			return None
		return a

	# POST a decoded JSON from a query
	@decode
	def requestPOST(self, req, data, contentType = False):
		formattedData = urllib.urlencode(data)
		try:
			r = Request(self.api_root + str(req), formattedData)
			r.add_header('Client-ID', self.cid)
			r.add_header('Accept', self.acc_head)
			if self.aut_tken != "":
				r.add_header('Authorization', "OAuth " + self.aut_tken)
			if self.contentType :
				r.add_header("Content-Type", "application/json")
			a = urlopen(r).read().decode("cp850")
		except HTTPError as ex:
			if ex.code == 400:
				print("Failed to authenticate. Is Client-ID correct? (HTTP/1.1 400)")
			else:
				print("An unexpected error occured: (HTTP/1.1 " + str(ex.code) + ")")
			return None
		return a		

	# PUT a decoded JSON from a query
	@decode
	def requestPUT(self, req, data, contentType = False):
		formattedData = urllib.urlencode(data)
		try:
			r = Request(self.api_root + str(req), formattedData)
			r.add_header('Client-ID', self.cid)
			r.add_header('Accept', self.acc_head)
			if self.aut_tken != "":
				r.add_header('Authorization', "OAuth " + self.aut_tken)
			if self.contentType :
				r.add_header("Content-Type", "application/json")
			r.get_method = lambda: "PUT"
			a = urlopen(r).read().decode("cp850")
		except HTTPError as ex:
			if ex.code == 400:
				print("Failed to authenticate. Is Client-ID correct? (HTTP/1.1 400)")
			else:
				print("An unexpected error occured: (HTTP/1.1 " + str(ex.code) + ")")
			return None
		return a

	# DELETE a decoded JSON from a query
	@decode
	def requestDELETE(self, req, data, contentType = False):
		formattedData = urllib.urlencode(data)
		try:
			r = Request(self.api_root + str(req), formattedData)
			r.add_header('Client-ID', self.cid)
			r.add_header('Accept', self.acc_head)
			if self.aut_tken != "":
				r.add_header('Authorization', "OAuth " + self.aut_tken)
			if self.contentType :
				r.add_header("Content-Type", "application/json")
			r.get_method = lambda: "DELETE"
			a = urlopen(r).read().decode("cp850")
		except HTTPError as ex:
			if ex.code == 400:
				print("Failed to authenticate. Is Client-ID correct? (HTTP/1.1 400)")
			else:
				print("An unexpected error occured: (HTTP/1.1 " + str(ex.code) + ")")
			return None
		return a

	# This returns a list because this is an API v3 thing, so get a user ID that is used for API v5
	def usersFromUsername(self, username):
		data = self.request("users?login=" + username)
		if data == None:
			return []
		if (data['_total'] == 0):
			return []
		else:
			users = data['users']
			ids = []
			for user in users:
				uid = str(user['_id'])
				ids.append(uid)
			return ids

	# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	#														#
	#	Twitch API v5, Channel feed 						#
	#														#
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # #

	def getMultipleFeedPosts(self, userID, cursor="", limit=0, comments=0):
		queryString = "feed/" + str(userID) + "/posts?"
		if limit != 0:
			queryString += "limit=" + str(limit) + "&"
		if cursor != "":
			queryString += "cursor=" + str(cursor) + "&"
		if comments != 0:
			queryString += "comments=" + str(comments)
		return self.request(queryString)

	def getFeedPost(self, userID, postID, comments=0):
		queryString = "feed/" + str(userID) + "/posts/" + str(postID)
		if comments != 0:
			queryString += "&comments=" + str(comments)
		return self.request(queryString)

	def createFeedPost(self, userID, content, share=None):
		data = {"content":str(content)}
		queryString = "feed/" + userID + "/posts"
		if share :
			data["share"] = "true"
		if self.aut_tken == "":
			raise ValueError("To create a post you must have a user authenticated")
		else:
			return self.requestPOST(queryString, data, True)

	def deleteFeedPost(self, userID, postID):
		data = {}
		queryString = "feed/" + str(userID) + "/posts/" + str(postID)
		if self.aut_tken == "":
			raise ValueError("To create a post you must have a user authenticated")
		else:
			return self.requestDELETE(queryString, data)

	def createFeedPostReaction(self, userID, postID, emote):
		data = {}
		queryString = "feed/" + str(userID) + "/posts/" + str(postID) + "?emote_id=" + str(emote)
		if self.aut_tken == "":
			raise ValueError("To create a reaction you must have a user authenticated")
		else:
			return self.requestPOST(queryString, data)

	def deleteFeedPostReaction(self, userID, postID, emote):
		data = {}
		queryString = "feed/" + str(userID) + "/posts/" + str(postID) + "?emote_id=" + str(emote)
		if self.aut_tken == "":
			raise ValueError("To delete a reaction you must have a user authenticated")
		else:
			return self.requestDELETE(queryString, data)

	def getFeedComments(self, userID, postID, cursor="", limit=0):
		queryString = "feed/" + str(userID) + "/posts/" + str(postID) + "/comments?"
		if limit != 0:
			queryString += "limit=" + str(limit) + "&"
		if cursor != "":
			queryString += "cursor=" + str(cursor) + "&"
		return self.request(queryString)

	def createFeedComment(self, userID, postID, content):
		data = {"content":str(content)}
		queryString = "feed/" + str(userID) + "/posts/" + str(postID) + "/comments"
		if self.aut_tken == "":
			raise ValueError("To create a feed comment you must have a user authenticated")
		else:
			return self.requestPOST(queryString, data, True)

	def deleteFeedComment(self, userID, postID, commentID):
		data = {}
		queryString = "feed/" + str(userID) + "/posts/" + str(postID) + "/comments/" + str(commentID)
		if self.aut_tken == "":
			raise ValueError("To delete a feed comment you must have a user authenticated")
		else:
			return self.requestPOST(queryString, data)

	def createFeedCommentReaction(self, userID, postID, commentID, emote):
		data = {}
		queryString = "feed/" + str(userID) + "/posts/" + str(postID) + "/comments/" + str(commentID) + "/reactions?emote_id=" + str(emote)
		if self.aut_tken == "":
			raise ValueError("To create a feed reaction you must have a user authenticated")
		else:
			return self.requestPOST(queryString, data)

	def deleteFeedCommentReaction(self, userID, postID, commentID, emote):
		data = {}
		queryString = "feed/" + str(userID) + "/posts/" + str(postID) + "?emote_id=" + str(emote)
		if self.aut_tken == "":
			raise ValueError("To delete a feed reaction you must have a user authenticated")
		else:
			return self.requestDELETE(queryString, data)


	# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	#														#
	#	Twitch API v5, Channels								#
	#														#
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # #

	def getChannel(self):
		if self.aut_tken == "":
			raise ValueError("To get a channel by OAuth token you must have a user authenticated")
		else:
			return self.request("channels")

	def getChannelByID(self, userID):
		queryString = "channels/" + str(userID)
		return self.request(queryString)

	def updateChannel(self, userID, status="", game="", delay="", channFeedEnabled=False):
		data = {}
		if status != "":
			data["status"] = status
		if game != "":
			data["game"] = game
		if delay != "":
			data["delay"] = delay
		if channFeedEnabled :
			data["channel_feed_enabled"] = "true"
		if data == {}:
			raise ValueError("To update a channel's properties you must have a user authenticated")
		else:
			queryString = "channels/" + str(userID)
			return self.requestPUT(queryString, data, True)

	def getChannelEditors(self, userID):
		queryString = "channels/" + str(userID) + "/editors"
		if self.aut_tken == "":
			raise ValueError("To get a channel's editors you must have a user authenticated")
		else:
			return self.request(queryString)

	def getChannelFollowers(self, userID, cursor="", limit=0, offset=0, direction=""):
		queryString = "channels/" + str(userID) + "/follows?"
		if limit != 0:
			queryString += "limit=" + str(limit) + "&"
		if cursor != "":
			queryString += "cursor=" + str(cursor) + "&"
		if offset != 0:
			queryString += "offset=" + str(offset)  + "&"
		if direction != "" and (direction == "asc" or direction == "desc"):
			queryString += "direction=" + str(direction)
		return self.request(queryString)

	def getChannelTeams(self, userID):
		queryString = "channels/" + str(userID) + "/teams"
		return self.request(queryString)

	def getChannelSubscribers(self, userID, limit=0, offset=0):
		queryString = "channels/" + str(userID) + "/subscriptions?"
		if limit != 0:
			queryString += "limit=" + str(limit) + "&"
		if offset != 0:
			queryString += "offset=" + str(offset)  + "&"
		if direction != "" and (direction == "asc" or direction == "desc"):
			queryString += "direction=" + str(direction)
		if self.aut_tken == "":
			raise ValueError("To get a channel's subscribers you must have a user authenticated")
		else:
			return self.request(queryString)

	def getChannelSubscriptionByUser(self, userID, subscriber):
		queryString = "channels/" + str(userID) + "/subscriptions/" + str(subscriber)
		if self.aut_tken == "":
			raise ValueError("To get a channel's subscribers you must have a user authenticated")
		else:
			return self.request(queryString)

	def isUserSubscribed(self, userID, subscriber):
		data = self.getChannelSubscriptionByUser(userID, subscriber)
		if data == None:
			return False
		elif "error" in data:
			return False
		else
			return True

	def getChannelVideos(self, userID, limit=0, offset=0, broadcastType=[], language=[], sort=""):
		queryString = "channels/" + str(userID) + "/videos?"
		if limit != 0:
			queryString += "limit=" + str(limit) + "&"
		if offset != 0:
			queryString += "offset=" + str(offset)  + "&"
		if len(broadcastType > 0):
			broadcastTypeStr = ""
			for item in broadcastType:
				if item in ["archive","highlight","upload"]:
					broadcastTypeStr += item + ","
			if broadcastTypeStr != "":
				queryString += "broadcast_type=" + str(broadcastTypeStr[:-1]) + "&"
		if len(language > 0):
			langStr = ""
			for item in broadcastType:
				langStr += item + ","
			if langStr != "":
				queryString += "broadcast_type=" + str(langStr[:-1]) + "&"
		if sort != "" and (sort == "views" or sort == "time"):
			queryString += "sort=" + str(direction)
		return self.request(queryString)

	def startChannelCommercial(self, userID, duration):
		if duration not in [30,60,90,120,150,180]:
			raise ValueError("Commercial duration must be one of 30, 60, 90, 120, 150, 180.")
		queryString = "channels/" + str(userID) + "/commercial"
		data = {"duration":str(duration)}
		if self.aut_tken == "":
			raise ValueError("To run a commercial you must have a user authenticated")
		else:
			return self.requestPOST(queryString, data, True)

	def resetStreamKey(self, userID):
		queryString = "channels/" + str(userID) + "/stream_key"
		data = {}
		if self.aut_tken == "":
			raise ValueError("To reset the stream key you must have a user authenticated")
		else:
			return self.requestDELETE(queryString, data)


	# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	#														#
	#	Twitch API v5, Chat	 								#
	#														#
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # #

	def getChatBadgesByChannel(self, userID):
		queryString = "chat/" + str(userID) + "/badges"
		return self.request(queryString)

	def getChatEmotesBySet(self, emoteSets=-1):
		queryString = "chat/emoticon_images"
		if emoteSets >= 0:
			queryString += "?emotesets=" + str(emoteSets)
		return self.request(queryString)

	def getAllChatEmoticons(self):
		return self.request("chat/emoticons")


	# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	#														#
	#	Twitch API v5, Games 								#
	#														#
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # #

	def getTopGames(self, limit=0, offset=0):
		queryString = "games/top?"
		if limit != 0:
			queryString += "limit=" + str(limit) + "&"
		if offset != 0:
			queryString += "offset=" + str(offset)  + "&"
		return self.request(queryString)


	# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	#														#
	#	Twitch API v5, Ingests 								#
	#														#
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # #

	def getIngestServerList(self):
		return self.request("ingests")


	# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	#														#
	#	Twitch API v5, Search 								#
	#														#
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # #

	def searchChannels(self, query, limit=0, offset=0):
		queryString = "search/channels?query=" + str(query)
		if limit != 0:
			queryString += "&limit=" + str(limit)
		if offset != 0:
			queryString += "&offset=" + str(offset)
		return self.request(queryString)

	def searchStreams(self, query, limit=0, offset=0, hls=None):
		queryString = "search/streams?query=" + str(query)
		if limit != 0:
			queryString += "&limit=" + str(limit)
		if offset != 0:
			queryString += "&offset=" + str(offset)
		if hls != None:
			queryString += "&hls=" + str(hls)
		return self.request(queryString)

	def searchGames(self, query, live=False):
		queryString = "search/games?query=" + str(query)
		if live :
			queryString += "&live=true"


	# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	#														#
	#	Twitch API v5, Streams 								#
	#														#
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # #

	def getStreamByChannel(self, userID, streamType=""):
		queryString = "streams/" + str(userID)
		if streamType in ["live","playlist","all"]:
			queryString += "?stream_type=" + streamType
		return self.request(queryString)

	def getAllStreams(self, game="", channel=[], streamType="", language="", limit=0, offset=0):
		queryString = "streams/?"
		if game != "":
			queryString += "game=" + str(game) + "&"
		if len(channel > 0):
			channStr = ""
			for item in channel:
				channStr += item + ","
			if channStr != "":
				queryString += "channel=" + str(channStr[:-1]) + "&"
		if streamType in ["live","playlist","all"]:
			queryString += "stream_type=" + str(streamType) + "&"
		if language != "":
			queryString += "language=" + str(language) + "&"
		if limit != 0:
			queryString += "limit=" + str(limit) + "&"
		if offset != 0:
			queryString += "offset=" + str(offset)
		return self.request(queryString)

	def getFollowedStreams(self, streamType="", limit=0, offset=0):
		queryString = "streams/followed?"
		if streamType in ["live","playlist","all"]:
			queryString += "stream_type=" + str(streamType) + "&"
		if language != "":
			queryString += "language=" + str(language) + "&"
		if limit != 0:
			queryString += "limit=" + str(limit) + "&"
		if offset != 0:
			queryString += "offset=" + str(offset)
		if self.aut_tken == "":
			raise ValueError("To get a channel's followed streams you must have a user authenticated")
		else:
			return self.request(queryString)

	def getFeaturedStreams(self, limit=0, offset=0):
		queryString = "streams/featured?"
		if limit != 0:
			queryString += "limit=" + str(limit) + "&"
		if offset != 0:
			queryString += "offset=" + str(offset)
		return self.request(queryString)

	def getStreamsSummary(self, game=""):
		queryString = "streams/summary"
		if game != ""
			queryString += "?game=" + str(game)
		return self.request(queryString)


	# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	#														#
	#	Twitch API v5, Teams 								#
	#														#
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # #

	def getAllTeams(self, limit=0, offset=0):
		queryString = "teams?"
		if limit != 0:
			queryString += "limit=" + str(limit) + "&"
		if offset != 0:
			queryString += "offset=" + str(offset)
		return self.request(queryString)

	def getTeam(self, team):
		queryString = "teams/" + str(team)
		return self.request(queryString)


	# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	#														#
	#	Twitch API v5, Users 								#
	#														#
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # #

	def getUser(self):
		if self.aut_tken == "":
			raise ValueError("To get a user you must have a user authenticated")
		else:
			return self.request("user")

	def getUserByID(self, userID):
		queryString = "users/" + str(userID)
		return self.request(queryString)

	def getUserEmotes(self, userID):
		queryString = "users/" + str(userID) + "/emotes"
		if self.aut_tken == "":
			raise ValueError("To get a users emotes you must have a user authenticated")
		else:
			return self.request(queryString)

	def getUserSubscriptionByChannel(self, userID, channel):
		queryString = "users/" + str(userID) + "/subscriptions/" + str(channel)
		if self.aut_tken == "":
			raise ValueError("To get a users emotes you must have a user authenticated")
		else:
			return self.request(queryString)

	def isUserSubscribedToChannel(self, userID, channel):
		data = getUserSubscriptionByChannel(userID, channel)
		if data == None:
			return False
		elif "error" in data:
			return False
		else
			return True

	def getUserFollows(self, userID, limit=0, offset=0, direction="",sortby=""):
		queryString = "users/" + str(userID) + "/follows/channels?"
		if limit != 0:
			queryString += "limit=" + str(limit) + "&"
		if offset != 0:
			queryString += "offset=" + str(offset) + "&"
		if direction in ["asc","desc"]:
			queryString += "direction=" + str(direction) + "&"
		if sortby in ["created_at","last_broadcast","login"]:
			queryString += "sortby=" + str(sortby)
		return self.request(queryString)

	def checkUserFollowsByChannel(self, userID, channel):
		queryString = "users/" + str(userID) + "/follows/channels/" + str(channel)
		return self.request(queryString)

	def isUserFollowingChannel(self, userID, channel):
		data = checkUserFollowsByChannel(userID, channel)
		if data == None:
			return False
		elif "error" in data:
			return False
		else
			return True

	def followChannel(self, userID, newChannel, notifications=False):
		data = {}
		queryString = "users/" + str(userID) + "/follows/channel/" + str(newChannel)
		if notifications:
			queryString += "?notifications=true"
		if self.aut_tken == "":
			raise ValueError("To follow a channel you must have a user authenticated")
		else:
			self.requestPUT(queryString, data)	# These return no data so we don't return anything

	def unfollowChannel(self, userID, channel):
		data = {}
		queryString = "users/" + str(userID) + "/follows/channel/" + str(newChannel)
		if self.aut_tken == "":
			raise ValueError("To unfollow a channel you must have a user authenticated")
		else:
			self.requestDELETE(queryString, data)	# These return no data so we don't return anything

	def getUserBlockList(self, userID, limit=0, offset=0):
		queryString = "users/" + str(userID) + "/blocks?"
		if limit != 0:
			queryString += "limit=" + str(limit) + "&"
		if offset != 0:
			queryString += "offset=" + str(offset)
		if self.aut_tken == "":
			raise ValueError("To get a user's block list you must have a user authenticated")
		else:
			return self.request(queryString)

	def blockUser(self, userID, newChannel):
		data = {}
		queryString = "users/" + str(userID) + "/blocks/" + str(newChannel)
		if self.aut_tken == "":
			raise ValueError("To block a user you must have a user authenticated")
		else:
			self.requestPUT(queryString, data)	# These return no data so we don't return anything

	def unblockUser(self, userID, channel):
		data = {}
		queryString = "users/" + str(userID) + "/blocks/" + str(newChannel)
		if self.aut_tken == "":
			raise ValueError("To unblock a user you must have a user authenticated")
		else:
			self.requestDELETE(queryString, data)	# These return no data so we don't return anything


	# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	#														#
	#	Twitch API v5, Users 								#
	#														#
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # #

	def getVideo(self, videoID):
		queryString = "videos/" + str(videoID)
		return self.request(queryString)

	def getTopVideos(self, limit=0, offset=0, game="", period="", broadcastType=[]):
		queryString = "videos/top?"
		if limit != 0:
			queryString += "limit=" + str(limit) + "&"
		if offset != 0:
			queryString += "offset=" + str(offset)  + "&"
		if game != "":
			queryString += "game=" + str(game) + "&"
		if period in ["month","week","all"]:
			queryString += "period=" + str(period) + "&"
		if len(broadcastType > 0):
			broadcastTypeStr = ""
			for item in broadcastType:
				if item in ["archive","highlight","upload"]:
					broadcastTypeStr += item + ","
			if broadcastTypeStr != "":
				queryString += "broadcast_type=" + str(broadcastTypeStr[:-1])

	def getFollowed(self, limit=0, offset=0, broadcastType=[]):
		queryString = "videos/followed?"
		if limit != 0:
			queryString += "limit=" + str(limit) + "&"
		if offset != 0:
			queryString += "offset=" + str(offset)  + "&"
		if len(broadcastType > 0):
			broadcastTypeStr = ""
			for item in broadcastType:
				if item in ["archive","highlight","upload"]:
					broadcastTypeStr += item + ","
			if broadcastTypeStr != "":
				queryString += "broadcast_type=" + str(broadcastTypeStr[:-1])
		if self.aut_tken == "":
			raise ValueError("To see a user's followed videos you must have a user authenticated")
		else:
			return self.request(queryString)

