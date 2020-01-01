# -*- coding: UTF-8 -*-

# @Date    : 2019/12/9
# @Author  : WANG JINGE
# @Email   : wang.j.au@m.titech.ac.jp
# @Language: python 3.7
"""

"""

from flask import redirect, render_template

from app.models import Tinyurl
from app.tinyurl.forms import UrlForm, SpecKeyForm
from . import bp
from .shorter import encode_ran_key, encode_spec_key
from ..limiter import limiter


@bp.route("/tiny", methods=['GET', 'POST'])
@limiter.limit("200/day")
def shorten():
    form = UrlForm()
    if form.validate_on_submit():
        url = form.url.data
        result = encode_ran_key(url)
        return render_template('tinyurl_result.html', tiny_url=result)
    return render_template('tinyurl.html', form=form)


@bp.route("/spec", methods=['GET', 'POST'])
@limiter.limit("50/day")
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
        url_db = Tinyurl.query.filter_by(url_key=key).first()
        if url_db:
            url = url_db.long_url
        else:
            return render_template('errors/404.html'), 404
        if '://' not in url:
            url = 'http://' + url
        return redirect(url)
