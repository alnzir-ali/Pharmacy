from flask import Flask, flash, redirect, render_template, request, session, url_for
from models import User, db
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# إعدادات قاعدة بيانات PostgreSQL (تأكد من مطابقة كلمة المرور الصحيحة لديك هنا)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'postgresql://postgres:admin%40123@localhost:5432/pharmacy_db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# إنشاء الجداول تلقائياً إذا لم تكن موجودة
with app.app_context():
  db.create_all()


@app.route('/')
def index():
  if 'user_id' not in session:
    return redirect(url_for('login'))
  return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password_hash, password):
      if not user.is_active:
        flash('هذا الحساب موقوف، يرجى مراجعة مدير النظام.', 'danger')
        return redirect(url_for('login'))

      session['user_id'] = user.id
      session['username'] = user.username
      session['role_id'] = user.role_id

      flash('تم تسجيل الدخول بنجاح!', 'success')
      return redirect(url_for('index'))
    else:
      flash('اسم المستخدم أو كلمة المرور غير صحيحة.', 'danger')

  return render_template('login.html')


@app.route('/logout')
def logout():
  session.clear()
  flash('تم تسجيل الخروج بنجاح.', 'info')
  return redirect(url_for('login'))


if __name__ == '__main__':
  app.run(debug=True)

  from models import Medicine, Role, User, db  # تأكد من استيراد Medicine


@app.route('/medicines')
def medicines_list():
  if 'user_id' not in session:
    return redirect(url_for('login'))

  # جلب كافة الأدوية من قاعدة البيانات
  medicines = Medicine.query.all()
  return render_template('medicines.html', medicines=medicines)

from datetime import datetime
from models import Medicine  # تأكد من استيراد Medicine


@app.route('/medicines/add', methods=['POST'])
def add_medicine():
  if 'user_id' not in session:
    return redirect(url_for('login'))

  try:
    name = request.form.get('name')
    scientific_name = request.form.get('scientific_name')
    category = request.form.get('category')
    price = request.form.get('price')
    cost_price = request.form.get('cost_price')
    stock_quantity = request.form.get('stock_quantity')
    expiry_date_str = request.form.get('expiry_date')
    barcode = request.form.get('barcode')

    # تحويل تاريخ الصلاحية من نص إلى Date
    expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d').date()

    new_med = Medicine(
        name=name,
        scientific_name=scientific_name,
        category=category,
        price=price,
        cost_price=cost_price if cost_price else None,
        stock_quantity=stock_quantity,
        expiry_date=expiry_date,
        barcode=barcode if barcode else None,
    )

    db.session.add(new_med)
    db.session.commit()
    flash('تم إضافة الدواء بنجاح!', 'success')
  except Exception as e:
    db.session.rollback()
    flash(f'حدث خطأ أثناء إضافة الدواء: {e}', 'danger')

  return redirect(url_for('medicines_list'))