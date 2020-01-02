# -*- coding: UTF-8 -*-

# @Date    : 2019/12/9
# @Author  : WANG JINGE
# @Email   : wang.j.au@m.titech.ac.jp
# @Language: python 3.7
"""

"""

from flask import current_app as app
from .. import redis_client
from app import db
from base62 import encode, decode
from app.models import Tinyurl


def decoder(url_key):
    return decode(url_key, charset=app.config['BASE62_CHARSET'])


# 每次检查是否曾经用过了
def check_set_key(url_key):
    used = Tinyurl.query.filter_by(url_key=url_key).first()
    if not used:
        return url_key
    while used:
        url_key = encode(int(used.id), charset=app.config['BASE62_CHARSET'])
        used = Tinyurl.query.filter_by(url_key=url_key).first()
    return url_key


def encode_ran_key(long_url):
    url_key = redis_client.get(long_url)
    if not url_key:
        tinyurl = Tinyurl(long_url=long_url)
        db.session.add(tinyurl)
        db.session.commit()
        url_key = encode(int(tinyurl.id), charset=app.config['BASE62_CHARSET'])
        tinyurl.url_key = check_set_key(url_key)
        db.session.commit()
        redis_client.set(long_url, tinyurl.url_key, ex=app.config['DB_EXPIRE_TIME'], nx=True)
    else:
        url_key = url_key.decode('utf8')

    return '{}/{}'.format(app.config['SERVER_URL_PREFIX'], url_key)


def get_exited_key(long_url):
    url_key = redis_client.get(long_url)
    if url_key:
        return url_key.decode('utf8')
    else:
        tinyurl = Tinyurl.query.filter_by(long_url=long_url).first()
        return tinyurl.url_key if tinyurl else None


def encode_spec_key(long_url, spec_key):
    url_key = get_exited_key(long_url)
    if url_key:
        decode_id = decoder(url_key)
        tinyurl = Tinyurl.query.get(decode_id)
    else:
        tinyurl = Tinyurl(long_url=long_url)
        db.session.add(tinyurl)
        db.session.commit()

    tinyurl.type = 'customize'
    tinyurl.url_key = spec_key
    db.session.commit()

    return '{}/{}'.format(app.config['SERVER_URL_PREFIX'], spec_key)
