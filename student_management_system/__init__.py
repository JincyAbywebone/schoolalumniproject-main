default_app_config = 'main_app.apps.MainAppConfig'

try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass