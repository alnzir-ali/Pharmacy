from app import app
from models import Role, User, db
from werkzeug.security import generate_password_hash


def create_admin():
  with app.app_context():
    # 1. قائمة الأدوار الافتراضية
    default_roles = [
        {'name': 'admin', 'display_name': 'مدير النظام'},
        {'name': 'pharmacist', 'display_name': 'صيدلي'},
        {'name': 'cashier', 'display_name': 'كاشير'},
        {'name': 'inventory_manager', 'display_name': 'مسؤول المخزون'},
        {'name': 'accountant', 'display_name': 'محاسب'},
    ]

    # 2. إدخال الأدوار إذا لم تكن موجودة
    for r_data in default_roles:
      role = Role.query.filter_by(name=r_data['name']).first()
      if not role:
        role = Role(name=r_data['name'], display_name=r_data['display_name'])
        db.session.add(role)
    db.session.commit()

    # 3. التحقق من وجود حساب مدير النظام
    admin_role = Role.query.filter_by(name='admin').first()
    existing_user = User.query.filter_by(username='admin').first()

    if existing_user:
      print('حساب مدير النظام موجود مسبقاً بالفعل.')
      return

    # 4. إنشاء حساب الأدمن الجديد
    hashed_password = generate_password_hash('admin123')
    new_admin = User(
        username='admin',
        email='admin@pharmacy.com',
        password_hash=hashed_password,
        full_name='مدير النظام العام',
        role_id=admin_role.id,
        branch_id=1,
        is_active=True,
    )

    db.session.add(new_admin)
    db.session.commit()
    print(
        'تم إنشاء الأدوار وإضافة حساب مدير النظام بنجاح!\nاسم المستخدم:'
        ' admin\nكلمة المرور: admin123'
    )


if __name__ == '__main__':
    create_admin()