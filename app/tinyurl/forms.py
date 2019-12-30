# -*- coding: UTF-8 -*-

# @Date    : 2019/12/11
# @Author  : WANG JINGE
# @Email   : wang.j.au@m.titech.ac.jp
# @Language: python 3.7
"""

"""

from flask_babel import _
from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length, ValidationError

from app.models import Tinyurl


class UrlForm(FlaskForm):
    url = StringField(_l('Url'),
                      validators=[
                          DataRequired(),
                          Length(min=0, max=500)
                      ])

    def validate_url(self, url):
        pass


class SpecKeyForm(FlaskForm):
    url = StringField(_l('Your URL'),
                      validators=[
                          DataRequired(),
                          Length(min=0, max=500)
                      ])
    speckey = StringField(_l('Customise Key'),
                          validators=[DataRequired(),
                                      Length(min=0, max=7)])

    def validate_url(self, url):
        pass

    def validate_speckey(self, speckey):
        spec_key = speckey.data
        if not spec_key.isalnum():
            raise ValidationError(_('Please only use alphabet or num or their combination'))

        used = Tinyurl.query.filter_by(url_key=spec_key).first()
        if used:
            raise ValidationError(_('Sorry, this url key is not available anymore'))
