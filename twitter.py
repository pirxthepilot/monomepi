import urllib
import urllib2
import json
import threading
import hmac
import hashlib
import base64
from time import sleep
from time import time
from os import urandom
from collections import OrderedDict

BEARER_TOKEN=
CONSUMER_KEY=
CONSUMER_SECRET=
TOKEN=
TOKEN_SECRET=
QCOUNT=30
QINTERVAL=240


class Tweets(object):

    def __init__(self, search_string='null'):
        self.since_id = 0
        self.search_string = search_string
        self.tweets = []

    def json_parse(self, jsontext):   # returns a list of dictionaries
        init_dict = json.loads(jsontext)
        relevant_list = []
##        self.since_id = str(init_dict[u'search_metadata'][u'max_id_str'])
##        for text in init_dict[u'statuses']:
##            relevant_dict = { 'screen_name' : str('@' + text[u'user'][u'screen_name']),
##                              'text'        : text[u'text'] }
##            relevant_list.append(relevant_dict)
        for text in init_dict:
            if int(self.since_id) < int(text[u'id']):
                self.since_id = str(text[u'id'])
            relevant_dict = { 'screen_name' : str('@' + text[u'user'][u'screen_name']),
                              'text'        : text[u'text'] }
            relevant_list.append(relevant_dict)
        return relevant_list

    def update(self, count):
        #url = 'https://api.twitter.com/1.1/search/tweets.json'
        url = 'https://api.twitter.com/1.1/statuses/home_timeline.json'
        #params = { 'q'      : str(self.search_string),
        #           'count'  : str(count),
        #           'lang'   : 'en',
        #           'result_type' : 'recent',
        #           'since_id' : self.since_id }

        params = { 'count'  : str(count) }
        if self.since_id <> 0:
            params['since_id'] = str(self.since_id)

        query = urllib.urlencode(params)
        #authmsg = 'Bearer ' + BEARER_TOKEN
        nonce = get_nonce()
        timestamp = str(int(time()))
        pstring = { 'oauth_consumer_key' : CONSUMER_KEY,
                    'oauth_nonce' : nonce,
                    'oauth_signature_method' : 'HMAC-SHA1',
                    'oauth_timestamp' : timestamp,
                    'oauth_token' : TOKEN,
                    'oauth_version' : '1.0' }
        pstring = dict(pstring.items() + params.items())
        
        basemsg = urllib.urlencode(OrderedDict(sorted(pstring.items(), key=lambda t: t[0])))
        basemsg = 'GET&' + urllib.quote_plus(url) + '&' + urllib.quote_plus(basemsg)
        #print basemsg
        signature = get_hmac_sig(basemsg, CONSUMER_SECRET + '&' + TOKEN_SECRET)

        authparams = { 'oauth_consumer_key' : CONSUMER_KEY,
                       'oauth_nonce' : nonce,
                       'oauth_signature' : signature,
                       'oauth_signature_method' : 'HMAC-SHA1',
                       'oauth_timestamp' : timestamp,
                       'oauth_token' : TOKEN,
                       'oauth_version' : '1.0' }
        authmsg = get_auth_string(authparams)

        url = url + '?' + query
        req = urllib2.Request(url)
        req.add_header('Authorization', authmsg)
        print url
        response = urllib2.urlopen(req)
        self.tweets.extend(self.json_parse(response.read()))

    def read_tweet(self, loc=0):
        if len(self.tweets) == 0:
            return False
        else:
            return self.tweets[loc]

    def grab_tweet(self):
        if len(self.tweets) == 0:
            return False
        else:
            return self.tweets.pop(0)   # Output in dict format


class TwitterThread(threading.Thread):

    def __init__(self, search_string='null'):
        threading.Thread.__init__(self)
        self.twitterdb = Tweets(str(search_string))
        self.exit_flag = False

    def run(self, count=QCOUNT, interval=QINTERVAL):    # count is no. of tweets to pull; interval is seconds between pulls
        while not self.exit_flag:
            #print 'Updating feed...',
            self.twitterdb.update(count)
            for i in range(interval):
                sleep(1)
                if self.exit_flag:
                    break
        print 'Twitter thread exit.'

    def call_exit(self):
        self.exit_flag = True


def get_hmac_sig(basemsg, key):
    hashfunc = hmac.new(key, '', hashlib.sha1)
    hashfunc.update(basemsg)
    return base64.b64encode(hashfunc.digest())

def get_nonce():
    random = urandom(64)
    return hashlib.md5(random).hexdigest()[:32]

def get_auth_string(authparams):
    out = 'OAuth '
    c = 0
    for key,value in OrderedDict(sorted(authparams.items(), key=lambda t: t[0])).items():
        c += 1
        out = out + urllib.quote_plus(key) + '="' + urllib.quote_plus(value) + '"'
        if c < len(authparams):
            out = out + ', '
    return out



if __name__=="__main__":
    Twit = Tweets()
    while True:
        #print 'Updating...'
        Twit.update(QCOUNT)
        for i in range(len(Twit.tweets)):
            if Twit.read_tweet():
                data = Twit.grab_tweet()    # read and delete the oldest tweet (first item in the list)
                print data['screen_name'], ': ', data['text']
                print '----'
                sleep(1)
