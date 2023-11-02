from flask import Flask, request
# render_template, redirect, url_for, session, flash
from backend.app.main.utility import response
from backend.app.main.utility import DBConnectivity
from user_service import User
from utility import response 

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secure secret key
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Change this to your database URI
# db = SQLAlchemy(app)
# bcrypt = Bcrypt(app)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check your credentials.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)