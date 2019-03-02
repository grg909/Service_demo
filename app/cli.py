import os
import click


def register(app):
    @app.cli.group()
    def translate():
        """翻译和本地化相关命令"""
        pass

    @translate.command()
    @click.argument('lang')
    def init(lang):
        """安装新的语言配置"""
        if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
            raise RuntimeError('extract command failed')
        if os.system(
                'pybabel init -i messages.pot -d app/translations -l ' + lang):
            raise RuntimeError('init command failed')
        os.remove('messages.pot')

    @translate.command()
    def update():
        """更新语言配置"""
        if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
            raise RuntimeError('extract command failed')
        if os.system('pybabel update -i messages.pot -d app/translations'):
            raise RuntimeError('update command failed')
        os.remove('messages.pot')

    @translate.command()
    def compile():
        """编译语言配置"""
        if os.system('pybabel compile -d app/translations'):
            raise RuntimeError('compile command failed')
