from flask_sqlalchemy import inspect
from app import create_app
from models import db, Patient, BedStatus, ChatHistory

def init_db():
    app = create_app()
    with app.app_context():
        # 删除所有表
        db.drop_all()
        print("表删除成功")
        
        # 创建所有表
        db.create_all()
        inspector = inspect(db.engine)
        print("表创建成功，当前表：", inspector.get_table_names())

        try:
            # 插入测试数据
            patient1 = Patient(name='张三')
            patient2 = Patient(name='李四')
            db.session.add_all([patient1, patient2])
            db.session.commit()
            print("测试数据插入成功：Patient 表中插入了 '张三' 和 '李四'")

            # 创建床位状态
            bed1 = BedStatus(bed_number=1, temperature=36.5, humidity=65, occupied=True, patient=patient1)
            bed2 = BedStatus(bed_number=2, temperature=36.8, humidity=62, occupied=True, patient=patient2)
            bed3 = BedStatus(bed_number=3, temperature=25.0, humidity=60, occupied=False)
            db.session.add_all([bed1, bed2, bed3])
            print("床位状态数据插入成功")

            # 创建聊天记录
            chat1 = ChatHistory(message='护士，我感觉有点不舒服', patient=patient1)
            chat2 = ChatHistory(message='好的，我马上过来查看', is_patient=False, patient=patient1)
            db.session.add_all([chat1, chat2])
            db.session.commit()
            print("聊天记录插入成功")

            print("数据库初始化完成")
        except Exception as e:
            db.session.rollback()
            print("数据插入失败，发生异常：", e)

if __name__ == '__main__':
    init_db()