# -*- coding: UTF-8 -*-

# @Date    : 2019/11/27
# @Author  : WANG JINGE
# @Email   : wang.j.au@m.titech.ac.jp
# @Language: python 3.7
"""

"""


from app import create_app


app = create_app()
app.app_context().push()
