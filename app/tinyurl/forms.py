# -*- coding: UTF-8 -*-

# @Date    : 2019/12/11
# @Author  : WANG JINGE
# @Email   : wang.j.au@m.titech.ac.jp
# @Language: python 3.7
"""

"""
from urllib import parse

from flask import current_app as app
from flask_babel import _
from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError


class UrlForm(FlaskForm):
    url = StringField(_l('Url'),
                      validators=[DataRequired(),
                                  Length(min=0, max=500)])

    def validate_url(self, url):
        pass


class SpecKeyForm(FlaskForm):
    url = StringField(_l('Url'),
                      validators=[DataRequired(),
                                  Length(min=0, max=500)])
    speckey = StringField(_l('Spec Key'),
                          validators=[DataRequired(),
                                      Length(min=0, max=7)])
    submit = SubmitField(_l('customize'))

    def validate_url(self, url):
        pass

    def validate_speckey(self, speckey):
        pass
