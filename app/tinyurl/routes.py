# -*- coding: UTF-8 -*-

# @Date    : 2019/12/9
# @Author  : WANG JINGE
# @Email   : wang.j.au@m.titech.ac.jp
# @Language: python 3.7
"""

"""

from flask import request, jsonify, redirect
from . import bp
from .shorter import urlShorter, check_url_avail

shorter = urlShorter()


@bp.route("/shortURL", methods=['POST'])
def shorten_request():
    url = request.get_data()
    chk_url_res = check_url_avail(url)
    if chk_url_res["State"] != "Success":
        return jsonify(chk_url_res)

    result = shorter.encode_ran_key(url)
    if result["State"] != "Success":
        return jsonify(result), 400
    return jsonify(result), 200


@bp.route("/specify/<specify_key>", methods=['POST'])
def specify_url_key(specify_key):
    url = request.get_data()
    chk_url_res = check_url_avail(url)
    if chk_url_res["State"] != "Success":
        return jsonify(chk_url_res)

    result = shorter.encode_spec_key(specify_key, url)
    if result["State"] != "Success":
        return jsonify(result), 400
    return jsonify(result), 200


@bp.route("/<url_key>")
def redirect_to_url(url_key):
    url = shorter.decode(url_key)
    if url is None:
        return jsonify({
            "State": "Failed",
            "Info": "url_key: '%s' is not in database" % (url_key)
        }), 404
    return redirect(url)
