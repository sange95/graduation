from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from info import create_app, db, models


# manage.py是程序启动入口，只关心启动的相关参数和内容，不关心具体该如何创建app或相关业务逻辑
# 此处调用info中的函数，会得到app
from info.models import User

app = create_app('development')
# 创建终端命令的对象
manager = Manager(app)
# 将app与db关联 # 使用迁移类,将应用和数据库连接对象保存起来
Migrate(app, db)
# 将移命令添加到manager中 # MigrateCommand：迁移的命令
manager.add_command('db', MigrateCommand)


@manager.option('-n', '-name', dest="name")
@manager.option('-p', '-password', dest="password")
def createsuperuser(name, password):
    if not all([name, password]):
        print("参数不足")
    user = User()
    user.nick_name = name
    user.mobile = name
    user.password = password
    user.is_admin = True

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
    print("添加成功")


if __name__ == '__main__':
    print(app.url_map)
    manager.run()
