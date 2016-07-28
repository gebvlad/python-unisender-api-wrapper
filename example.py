#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import unisender
from unisender import call
from uuid import uuid4

# your api-key
unisender.api_key = '<YOUR_API_KEY>'

# language
unisender.lang = 'ru'

your_email = 'some-verified-email@rarus.ru'

rand_string = str(uuid4())

try:
    # create new sender list http://goo.gl/dgVsVo
    res = call('createList', {
        'title': 'Your test sender list #' + rand_string
    })

    list_id = res['result']['id']

    print 'Created list: ', list_id

    # import subscribers to sender list https://goo.gl/JrE7Qa
    res = call('importContacts', {
        'field_names': [
            'email', 'email_subscribe_times', 'email_list_ids'
        ],
        'data':        [
            [
                'some-user-for-sender-list@example.com', '2016-07-26', list_id
            ]
        ]
    })

    print 'Import subscribers finished: ', res['result']

    # create new message https://goo.gl/SaNx3k
    res = call('createEmailMessage', {
        'sender_name':  'Some Username',
        'sender_email': your_email,
        'subject':      'Some subject with random string #' + rand_string,
        'body':         'Some text message',
        'list_id':      list_id,
    })

    message_id = res['result']['message_id']

    print 'Created message: ', message_id

    # send test message to verified user https://goo.gl/AKop7u
    res = call('sendTestEmail', {
        'email': your_email,
        'id':    message_id
    })

    # print sending result
    print res['result']['message']
except TypeError as err:
    print err
