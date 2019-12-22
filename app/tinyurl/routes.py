# -*- coding: UTF-8 -*-

# @Date    : 2019/12/9
# @Author  : WANG JINGE
# @Email   : wang.j.au@m.titech.ac.jp
# @Language: python 3.7
"""

"""

from flask import jsonify, redirect, render_template

from app.models import Tinyurl
from app.tinyurl.forms import UrlForm, SpecKeyForm
from . import bp
from .shorter import encode_ran_key, decoder, encode_spec_key


@bp.route("/shorten", methods=['GET', 'POST'])
def shorten():
    form = UrlForm()
    if form.validate_on_submit():
        url = form.url.data
        result = encode_ran_key(url)
        return render_template('tinyurl_result.html', tiny_url=result)
    return render_template('tinyurl.html', form=form)


@bp.route("/specify", methods=['GET', 'POST'])
def specify():
    form = SpecKeyForm()
    if form.validate_on_submit():
        url = form.url.data
        spec_key = form.speckey.data
        result = encode_spec_key(url, spec_key)
        return render_template('tinyurl_result.html', tiny_url=result)
    return render_template('tinyurl_customize.html', form=form)


@bp.route("/<key>")
def redirect_to_url(key):
    if not key.isalnum():
        return render_template('errors/404.html'), 404
    else:
        decode_id = decoder(key)
        url_db = Tinyurl.query.get(decode_id)
        if url_db:
            url = url_db.long_url
        else:
            return render_template('errors/404.html'), 404
        if '://' not in url:
            url = 'http://' + url
        return redirect(url)
