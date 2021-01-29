import click
from flask import Flask
from .extensions import db
from .models import Product, SoloPiFile, SoloPiTag
from .views import solo_bp


def create_app():
    app = Flask('solopi')
    app.config.from_pyfile('settings.py')
    register_commands(app)
    register_shell_context(app)
    db.init_app(app)
    app.register_blueprint(solo_bp, url_prefix='/')
    return app


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, Product=Product, SoloPiFile=SoloPiFile, SoloPiTag=SoloPiTag)


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm(
                'This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    def initsolopi():
        """Initialize the solopi."""
        db.drop_all()
        click.echo("Drop tables.")
        db.create_all()
        click.echo("Initialized database.")
        csv_title_cn = {
            '累计全局上行流量': 'global_uplink',
            '累计全局下行流量': 'global_downlink',
            '累计应用上行流量': 'app_uplink',
            '累计应用下行流量': 'app_downlink',
            '平均电流': 'average_battery',
            '全局上行速率': 'global_uplink_speed',
            '全局下行速率': 'global_downlink_speed',
            '全局占用_CPU': 'CPU',
            '全局占用_Memory': 'memory',
            '实时电流': 'Real_time_battery',
            '刷新耗时': 'refresh_time_consuming',
            '响应耗时': 'response_time_consuming',
            '延迟次数': 'Delay_times',
            '延迟占比': 'Delay_ratio',
            '应用进程-appbrand0-3030': 'Application_process',
            '应用上行速率': 'app_uplink_speed',
            '应用下行速率': 'app_downlink_speed',
            '帧率': 'FPS',
            '最长延迟时间': 'Maximum_delay_time',
            'PrivateDirty内存-appbrand0-3030': 'PrivateDirty',
            'PSS内存-appbrand0-3030': 'PSS'}
        csv_title_en = {
            'global_uplink': '累计全局上行流量(KB)',
            'global_downlink': '累计全局下行流量(KB)',
            'app_uplink': '累计应用上行流量(KB)',
            'app_downlink': '累计应用下行流量(KB)',
            'average_battery': '平均电流(mA)',
            'global_uplink_speed': '全局上行速率(KB)',
            'global_downlink_speed': '全局下行速率(KB)',
            'CPU': '全局占用(%)',
            'memory': '全局占用(MB)',
            'Real_time_battery': '实时电流(mA)',
            'refresh_time_consuming': '刷新耗时(ms)',
            'response_time_consuming': '响应耗时(ms)',
            'Delay_times': '延迟次数(次)',
            'Delay_ratio': '延迟占比(%)',
            'Application_process': '应用进程-appbrand0-3030(%)',
            'app_uplink_speed': '应用上行速率(KB)',
            'app_downlink_speed': '应用下行速率(KB)',
            'FPS': '帧率(帧)',
            'Maximum_delay_time': '最长延迟时间(ms)',
            'PrivateDirty': 'PrivateDirty内存-appbrand0-3030(MB)',
            'PSS': 'PSS内存-appbrand0-3030(MB)'
        }
        for k, v in csv_title_cn.items():
            solo = SoloPiTag(cn_name=k, en_name=v, csv_title=csv_title_en[v])
            print(k, v)
            db.session.add(solo)
        db.session.commit()
        click.echo('Done.')
