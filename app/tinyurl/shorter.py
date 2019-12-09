# -*- coding: UTF-8 -*-

# @Date    : 2019/12/9
# @Author  : WANG JINGE
# @Email   : wang.j.au@m.titech.ac.jp
# @Language: python 3.7
"""

"""

from flask import current_app

import redis
import urllib.parse as parse
import hashlib
import base62


def short(url):
    return base62.encodebytes(hashlib.md5(url).digest()[-4:])


def check_url_avail(url):
    if len(url) > current_app.config['MAX_URL_LEN']:
        return {
            "State": "Failed",
            "Error_msg": "Please don't use url longer than 2000 character."
        }
    parsed_url = parse.urlparse(url.decode())
    if parsed_url.scheme == '':
        return {
            "State":
                "Failed",
            "Error_msg":
                "Please use correct protocol such as 'http', 'https' or 'ftp'."
        }
    return {"State": "Success"}


def check_url_loop(url_key, url):
    # avoid make a tiny url directed to it self
    parsed_url = parse.urlparse(url.decode())
    url_path = parsed_url.path.replace("/", "")
    server_domain = parse.urlparse(
        current_app.config['SERVER_URL_PREFIX']).netloc
    if server_domain == parsed_url.netloc and url_path == url_key:
        return {
            "State":
                "Failed",
            "Error_msg":
                "This url %s will redirect to same page" %
                (current_app.config['SERVER_URL_PREFIX'] + url_key)
        }
    return {"State": "Success"}


class urlShorter:

    def __init__(self):
        self.db = redis.Redis(host=current_app.config['REDIS_URL'],
                              db=0,
                              decode_responses=True)

    def decode(self, short_key):
        return self.db.get(short_key)

    def set_db(self, url_key, long_url):
        try:
            self.db.set(url_key, long_url)
        except Exception as e:
            raise RuntimeError("Redis set data error", e)

    def encode_ran_key(self, long_url):
        url_key = short(long_url)

        return self.set_db(url_key, long_url)

    def encode_spec_key(self, spec_key, long_url):

        chk_loop_res = check_url_loop(spec_key, long_url)
        if chk_loop_res["State"] != "Success":
            return chk_loop_res

        # Check if the given key has been used
        get_res = self.decode(spec_key)
        if get_res is not None:
            # Given key has been used, check if the key has same url
            if get_res != long_url:
                # Not same, generate another key for it.
                res = self.encode_ran_key(long_url)
                res["Info"] = "The given key %s is not avaiable, but we generate another usable key for you." % (
                    spec_key)
                return res
        else:
            # Given key hasn't been used, insert it.
            set_res = self.set_db(spec_key, long_url)
            if set_res["State"] != "Success":
                return set_res

        return {"State": "Success",
                "short_url": "%s/%s" % (current_app.config['SERVER_URL_PREFIX'], spec_key)}