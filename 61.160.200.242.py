#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2, urllib, random, struct, threading, time, string
import gevent
from gevent import monkey

from randstr import *


class RedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        result = urllib2.HTTPError(req.get_full_url(), code, msg, headers, fp)
        result.status = code
        return result
    http_error_301 = http_error_303 = http_error_307 = http_error_302


def request():
    redirect = 'http://' + gen_random_domain()
    print redirect
    url = 'http://61.160.200.242:7701/stat.log.redirect?url=' + urllib.quote_plus(redirect)
    # values = {'idType' : random.randint(1,3) }
    # data = urllib.urlencode(values)
    # print str(values)
    opener = urllib2.build_opener(RedirectHandler)
    opener.addheaders = [('User-Agent', random.choice(USER_AGENT_DATA))]
    urllib2.install_opener(opener)
    try:
        response =urllib2.urlopen(url)
        page = response.read()
        # print page
    except Exception as what:
        print what.message


class WorkerThread(threading.Thread):
    def __init__(self):
        super(WorkerThread, self).__init__()

    def run(self):
        for i in xrange(1, 10000):
            request()


monkey.patch_all()

workers = []
for i in xrange(1, 100):
    worker = WorkerThread()
    worker.start()
    workers.append(worker)

for worker in workers:
    worker.join()
    print 'worker finished'

# request()


while False:
    try:
        time.sleep(random.randint(1,3))
        request()
    except Exception:
        pass
