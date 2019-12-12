# -*- coding: UTF-8 -*-

# @Date    : 2019/12/9
# @Author  : WANG JINGE
# @Email   : wang.j.au@m.titech.ac.jp
# @Language: python 3.7
"""

"""

from flask import request, jsonify, redirect, render_template

from app.models import Tinyurl
from app import db
from app.tinyurl.forms import UrlForm
from . import bp
from .shorter import check_url_avail, valid_key, encode_ran_key
from base62 import decode
from ..cache import cache


@bp.route("/shorten", methods=['GET', 'POST'])
def shorten():
    form = UrlForm()
    if form.validate_on_submit():
        url = form.url.data
        result = encode_ran_key(url)
        return jsonify(result)
    return render_template('tinyurl.html', form=form)


@bp.route("/<key>")
@cache.cached(timeout=50)
def redirect_to_url(key):
    if not valid_key(key):
        return jsonify({
            "State": "Failed",
            "Info": "url_key: '%s' is a not valid key" % (key)
        }), 404
    else:
        decode_id = decode(str(key))
        print(decode_id)
        url_db = Tinyurl.query.get(decode_id)
        if url_db:
            url = url_db.long_url
        else:
            return jsonify({
                "State": "Failed",
                "Info": "url_key: '%s' is not available" % (key)
            }), 404
        if '://' not in url:
            url = 'http://' + url
        return redirect(url)


# @bp.route("/specify/<specify_key>", methods=['POST'])
# def specify_url_key(specify_key):
#     url = request.get_data()
#     chk_url_res = check_url_avail(url)
#     if chk_url_res["State"] != "Success":
#         return jsonify(chk_url_res)
#
#     result = encode_spec_key(specify_key, url)
#     if result["State"] != "Success":
#         return jsonify(result), 400
#     return jsonify(result), 200
