import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config():
    # 密钥设定
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'

    # 邮件服务器配置
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = os.environ.get('MAIL_ADMINS')

    # 每页数据列表长度
    POSTS_PER_PAGE = 5

    # 语言支持
    LANGUAGES = ['en', 'zh']
    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')

    # Heroku log
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

    # 消息队列
    WORKER_NAME = 'grg909-task1'

    # Tiny url service
    SERVER_URL_PREFIX = os.getenv("SERVER_URL_PREFIX",
                                  "[Put your IP/domain name Here]")
    MAX_URL_LEN = int(os.getenv("MAX_URL_LEN", "200"))
    DB_EXPIRE_TIME = int(os.getenv("DB_EXPIRE_TIME", "31536000"))
    BASE62_CHARSET = os.getenv("BASE62_CHARSET", 'iPFJm70Hxb58t2qSsDhpeCULjIY43QrkTw96lWNZoBOKVXRgaMG1nfuEyvAczd')

    CACHE_CONFIG = {
        'CACHE_TYPE': 'redis',
        'CACHE_KEY_PREFIX': 'url',
        'CACHE_REDIS_URL': REDIS_URL
    }
