from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# جدول الأدوار (Roles)
class Role(db.Model):
  __tablename__ = 'roles'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), unique=True, nullable=False)
  display_name = db.Column(db.String(100), nullable=False)
  users = db.relationship('User', backref='role', lazy=True)


# جدول الصلاحيات (Permissions)
class Permission(db.Model):
  __tablename__ = 'permissions'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), unique=True, nullable=False)
  module = db.Column(db.String(50), nullable=False)
  description = db.Column(db.Text)


# جدول ربط الأدوار بالصلاحيات
role_permissions = db.Table(
    'role_permissions',
    db.Column(
        'role_id',
        db.Integer,
        db.ForeignKey('roles.id', ondelete='CASCADE'),
        primary_key=True,
    ),
    db.Column(
        'permission_id',
        db.Integer,
        db.ForeignKey('permissions.id', ondelete='CASCADE'),
        primary_key=True,
    ),
)


# جدول المستخدمين (Users)
class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(50), unique=True, nullable=False)
  email = db.Column(db.String(100), unique=True, nullable=False)
  password_hash = db.Column(db.String(255), nullable=False)
  full_name = db.Column(db.String(100), nullable=False)
  role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
  branch_id = db.Column(db.Integer, default=1)
  is_active = db.Column(db.Boolean, default=True)
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  audit_logs = db.relationship('AuditLog', backref='user', lazy=True)


# جدول إعدادات الصيدلية العامة (Settings)
class Setting(db.Model):
  __tablename__ = 'settings'
  id = db.Column(db.Integer, primary_key=True)
  key_name = db.Column(db.String(100), unique=True, nullable=False)
  key_value = db.Column(db.Text, nullable=False)
  description = db.Column(db.Text)


# جدول سجل التدقيق الأمني (Audit Logs)
class AuditLog(db.Model):
  __tablename__ = 'audit_logs'
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  action = db.Column(db.String(100), nullable=False)
  table_name = db.Column(db.String(50))
  record_id = db.Column(db.Integer)
  details = db.Column(db.Text)
  ip_address = db.Column(db.String(45))
  created_at = db.Column(db.DateTime, default=datetime.utcnow)

  # جدول الأدوية والمخزون (Medicines)
class Medicine(db.Model):
    __tablename__ = 'medicines'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)            # اسم الدواء التجاري
    scientific_name = db.Column(db.String(150))                # الاسم العلمي
    category = db.Column(db.String(100))                       # التصنيف (مسكن، مضاد حيوي، إلخ)
    price = db.Column(db.Numeric(10, 2), nullable=False)       # سعر البيع
    cost_price = db.Column(db.Numeric(10, 2))                  # سعر الشراء
    stock_quantity = db.Column(db.Integer, default=0)          # الكمية المتوفرة
    expiry_date = db.Column(db.Date, nullable=False)           # تاريخ الصلاحية
    barcode = db.Column(db.String(50), unique=True)            # الباركود
    created_at = db.Column(db.DateTime, default=datetime.utcnow)