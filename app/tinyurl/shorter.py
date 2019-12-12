# -*- coding: UTF-8 -*-

# @Date    : 2019/12/9
# @Author  : WANG JINGE
# @Email   : wang.j.au@m.titech.ac.jp
# @Language: python 3.7
"""

"""

from flask import current_app as app

import urllib.parse as parse
from app import db
import base62

from app.models import Tinyurl


def valid_key(key):
    if key.isalnum():
        return True
    return False


def check_url_avail(url):
    if len(url) > app.config['MAX_URL_LEN']:
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
    server_domain = parse.urlparse(app.config['SERVER_URL_PREFIX']).netloc
    if server_domain == parsed_url.netloc and url_path == url_key:
        return {
            "State":
                "Failed",
            "Error_msg":
                "This url %s will redirect to same page" %
                (app.config['SERVER_URL_PREFIX'] + url_key)
        }
    return {"State": "Success"}


def encode_ran_key(url):
    url_key = app.redis.get(url)
    if not url_key:
        tinyurl = Tinyurl(long_url=url)
        db.session.add(tinyurl)
        db.session.commit()
        url_key = base62.encode(int(tinyurl.id))
        app.redis.set(url, url_key, ex=86400, nx=True)

    return {
        "State": "Sucess",
        "short_url": "%s/%s" % (app.config['SERVER_URL_PREFIX'], url_key)
    }

# def encode_spec_key(spec_key, long_url):
#
#     chk_loop_res = check_url_loop(spec_key, long_url)
#     if chk_loop_res["State"] != "Success":
#         return chk_loop_res
#
#     # Check if the given key has been used
#     get_res = self.decode(spec_key)
#     if get_res is not None:
#         # Given key has been used, check if the key has same url
#         if get_res != long_url:
#             # Not same, generate another key for it.
#             res = encode_ran_key(long_url)
#             res["Info"] = "The given key %s is not avaiable, but we generate another usable key for you." % (
#                 spec_key)
#             return res
#     else:
#         # Given key hasn't been used, insert it.
#         set_res = self.set_db(spec_key, long_url)
#         if set_res["State"] != "Success":
#             return set_res
#
#     return {
#         "State": "Success",
#         "short_url": "%s/%s" % (app.config['SERVER_URL_PREFIX'], spec_key)
#     }
