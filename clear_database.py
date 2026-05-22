from flask import Flask
from db import db
import os
import sys

# 添加当前目录到路径
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# 创建Flask应用
app = Flask(__name__)

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rfid_system_new.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your-secret-key-here'

# 初始化数据库
db.init_app(app)

# 延迟导入模型，避免循环依赖
class Models:
    Product = None
    Barcode = None
    RFID = None
    Category = None
    SubCategory = None
    Color = None

def init_models():
    global Models
    from models.product import Product
    from models.barcode import Barcode
    from models.rfid import RFID
    from models.category import Category, SubCategory
    from models.color import Color
    Models.Product = Product
    Models.Barcode = Barcode
    Models.RFID = RFID
    Models.Category = Category
    Models.SubCategory = SubCategory
    Models.Color = Color

# 清空数据库
def clear_database():
    with app.app_context():
        # 初始化模型
        init_models()
        
        print("开始清空数据库...")
        
        try:
            # 清空所有表，注意顺序，先清空子表，再清空父表
            tables = [
                Models.RFID,
                Models.Barcode,
                Models.Product,
                Models.Color,
                Models.SubCategory,
                Models.Category
            ]
            
            for model in tables:
                table_name = model.__tablename__
                print(f"清空表: {table_name}")
                # 清空表数据
                model.query.delete()
                # 重置id自增，使用text()函数执行原生SQL，处理sqlite_sequence可能不存在的情况
                from sqlalchemy import text
                try:
                    db.session.execute(text(f'DELETE FROM sqlite_sequence WHERE name="{table_name}"'))
                except Exception as e:
                    print(f"重置表 {table_name} 的ID失败（可能没有AUTOINCREMENT）：{str(e)}")
            
            # 提交事务
            db.session.commit()
            print("数据库已成功清空！")
        except Exception as e:
            db.session.rollback()
            print(f"清空数据库失败：{str(e)}")
        finally:
            db.session.close()

if __name__ == '__main__':
    clear_database()