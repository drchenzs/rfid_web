from db import db
from app import init_models, app

with app.app_context():
    init_models()
    db.create_all()
    print("数据库初始化完成！")
