# In consumers.py
from channels import Channel, Group
from channels.sessions import channel_session
from .models import ChatMessage
import json


# Connected to chat-messages
def msg_consumer(message):
	print("msg_consumer")
	print(message.content)
	# Save to model
	room = message.content['room']
	ChatMessage.objects.create(
		room=room,
		message=message.content['message'],
	)
	# Broadcast to listening sockets
	Group("chat-%s" % room).send({
		"text": message.content['message'],
	})


# Connected to websocket.connect
@channel_session
def ws_connect(message):
	print("ws_connect")
	print(message.content)
	# Work out room name from path (ignore slashes)
	room = message.content['path'].strip("/")
	# Save room in session and add us to the group
	message.channel_session['room'] = room
	Group("chat-%s" % room).add(message.reply_channel)


# Connected to websocket.receive
@channel_session
def ws_message(message):
	print("ws_connect")
	print(message.content)

	data = json.loads(message.content['text'])
	text = data['text']
	user = "Anonymous" if data['user'].startswith("Anonymous_") else data['user']
	room = message.channel_session['room']

	print(text)
	print(user)
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
	Group("chat-%s" % message.channel_session['room']).discard(message.reply_channel)
