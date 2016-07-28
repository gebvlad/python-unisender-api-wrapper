#!/usr/bin/env python
#  -*- coding: utf-8 -*-
import json

try:
    import requests
    import requests.adapters
except ImportError:
    requests = None
    raise ImportError('Not found module requests\nrun: pip install requests')

# Unisender API key
api_key = None

# Language for response: ru - russian, en - english, it - italian
lang = 'ru'

# Unisender API endpoint
api_url = 'http://api.unisender.com/%s/api/%s?format=json'

# Timeout for API request in seconds
timeout = 60

# Retries for API request
requests.adapters.DEFAULT_RETRIES = 10


def call(method, params):
    """
    Call Unisender API method name

    :param method: API method name for calling
    :param params: Params for calling
    :return: dict API response
    """

    if lang not in ('ru', 'en', 'it'):
        raise Exception('Unsupported language')

    if method == '' or not isinstance(method, basestring):
        raise Exception('Empty Method')

    if api_key is None:
        raise Exception('Empty API-key')

    # Add API-key to params
    params['api_key'] = api_key

    params = prepare_params(params)

    # request url
    url = api_url % (lang, method)

    r = {}

    try:
        # make request
        r = requests.post(url, params=params, timeout=timeout)
        result = json.loads(r.text)
    except ValueError:
        result = dict(error='Error on decode api response [' + r.text + ']')
    except requests.exceptions.ReadTimeout:
        result = dict(error='Timeout waiting expired [' + str(timeout) + ' sec]')
    except requests.exceptions.ConnectionError:
        result = dict(error='Max retries exceeded [' + str(requests.adapters.DEFAULT_RETRIES) + ']')

    return result


def prepare_params(params):
    """
    Prepare parameters for request

    Convert params from
    {
        'key1': 'val1',
        'key2': ['val2_1', 'val2_2'],
        'key3': [
            ['val3_1', 'val3_2']
        ],
    }
    to
    {
        'key1':      'val1',
        'key2[0]':   'val2_1',
        'key2[1]':   'val2_2',
        'key3[0][0]':'val3_1'
        'key3[0][1]':'val3_2'
    }
    it is needed by Unisender documentation

    :param params: dict Parameters of request
    :return: dict Linear dict og parameters
    """
    params_str = dict()

    for i in params:
        if isinstance(params[i], list):
            count_j = 0
            for j in params[i]:
                count_z = 0
                if isinstance(j, list):
                    for z in j:
                        params_str[i + '[' + str(count_j) + '][' + str(count_z) + ']'] = z
                        count_z += 1
                else:
                    params_str[i + '[' + str(count_j) + ']'] = j
                count_j += 1
        else:
            params_str[i] = params[i]

    return params_str
