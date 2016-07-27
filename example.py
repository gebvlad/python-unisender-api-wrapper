#!/usr/bin/env python
#  -*- coding: utf-8 -*-

from unisender import call
from uuid import uuid4

# your api-key
key = '<YOUR_API_KEY>'

rand_string = str(uuid4())

# create new sender list http://goo.gl/dgVsVo
res = call('createList', {
    'api_key': key,
    'title':   'Your test sender list #' + rand_string
}, 'ru')

list_id = res['result']['id']

# import subscribers to sender list https://goo.gl/JrE7Qa
call('importContacts', {
    'api_key':     key,
    'field_names': [
        'email', 'email_subscribe_times', 'email_list_ids'
    ],
    'data':        [
        [
            'some-user-for-sender-list@example.com', '2016-07-26', list_id
        ]
    ]
})

# create new message https://goo.gl/SaNx3k
res = call('createEmailMessage', {
    'api_key':      key,
    'sender_name':  'Some Username',
    'sender_email': 'some-verified-user@example.com',
    'subject':      'Some subject with random string #' + rand_string,
    'body':         'Some text message',
    'list_id':      list_id,
})

message_id = res['result']['message_id']

# send test message to verified user https://goo.gl/AKop7u
res = call('sendTestEmail', {
    'api_key': key,
    'email':   'some-verified-user@example.com',
    'id':      message_id
})

# print sending result
print res['result']['message']
