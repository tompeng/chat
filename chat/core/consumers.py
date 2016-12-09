# In consumers.py
from channels import Channel, Group
from channels.sessions import channel_session
from .models import ChatMessage
import json


# Connected to websocket.connect
@channel_session
def ws_connect(message):
	print("ws_connect")

	# Work out room name from path (ignore slashes)
	room = message.content['path'].strip("/")

	print(room)
	# Save room in session and add us to the group
	message.channel_session['room'] = room
	Group("chat-%s" % room).add(message.reply_channel)


# Connected to websocket.receive
@channel_session
def ws_message(message):
	print("ws_connect")

	data = json.loads(message.content['text'])
	text = data['text']
	user = "Anonymous" if data['user'].startswith("Anonymous_") else data['user']
	room = message.channel_session['room']

	print(room)

	ChatMessage.objects.create(
		room=room,
		message=text,
		user=user
	)
	# Broadcast to listening sockets
	Group("chat-%s" % room).send({
		"text": message.content['text'],
	})


# Connected to websocket.disconnect
@channel_session
def ws_disconnect(message):
	print("ws_disconnect")
	Group("chat-%s" % message.channel_session['room']).discard(message.reply_channel)
