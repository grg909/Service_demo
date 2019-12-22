# -*- coding: UTF-8 -*-

# @Date    : 2019/12/9
# @Author  : WANG JINGE
# @Email   : wang.j.au@m.titech.ac.jp
# @Language: python 3.7
"""

"""

from flask import current_app as app

from app import db
from base62 import encode, decode

from app.models import Tinyurl


def decoder(url_key):
    return decode(url_key, charset=app.config['BASE62_CHARSET'])


# 每次生成
def check_set_key(url_key):
    used = Tinyurl.query.filter_by(url_key=url_key).first()
    if used and used.type == 'customize':
        return encode(int(used.id), charset=app.config['BASE62_CHARSET'])
    else:
        return url_key


def encode_ran_key(long_url):
    url_key = app.redis.get(long_url)
    if not url_key:
        tinyurl = Tinyurl(long_url=long_url)
        db.session.add(tinyurl)
        db.session.commit()
        url_key = encode(int(tinyurl.id), charset=app.config['BASE62_CHARSET'])
        tinyurl.url_key = check_set_key(url_key)
        db.session.commit()
        app.redis.set(long_url, tinyurl.url_key, ex=86400, nx=True)

    return '{}/{}'.format(app.config['SERVER_URL_PREFIX'], url_key)


def get_exited_key(long_url):
    url_key = app.redis.get(long_url)
    if url_key:
        return url_key
    else:
        tinyurl = Tinyurl.query.filter_by(long_url=url_key).first()
        return tinyurl.url_key if tinyurl else None


def encode_spec_key(long_url, spec_key):
    url_key = get_exited_key(long_url)
    spec_id = decoder(spec_key)
    if url_key:
        decode_id = decoder(url_key)
        tinyurl = Tinyurl.query.get(decode_id)
    else:
        tinyurl = Tinyurl(long_url=long_url)
        db.session.add(tinyurl)
        db.session.commit()

    if spec_id < tinyurl.id:
        return 'Sorry, this tiny url is not available anymore, please try another'
    elif spec_id == tinyurl.id:
        return 'keep use it'
    else:
        tinyurl.type = 'customize'
        tinyurl.url_key = spec_key
        db.session.commit()

    return '{}/{}'.format(app.config['SERVER_URL_PREFIX'], spec_key)
