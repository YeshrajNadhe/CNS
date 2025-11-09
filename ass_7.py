from flask import Flask, request, render_template_string, redirect, url_for, flash
import bcrypt

app = Flask(__name__)
app.secret_key = "1234"   # needed for flash messages

# simple in-memory database
users = {}

# HTML pages (very simple)
home_page = """
<h2>Welcome to Secure Website</h2>
<a href="/register">Register</a> | <a href="/login">Login</a>
"""

register_page = """
<h2>Register Page</h2>
<form method="post">
  Username: <input name="username"><br><br>
  Password: <input type="password" name="password"><br><br>
  <input type="submit" value="Register">
</form>
<a href="/">Back</a>
"""

login_page = """
<h2>Login Page</h2>
<form method="post">
  Username: <input name="username"><br><br>
  Password: <input type="password" name="password"><br><br>
  <input type="submit" value="Login">
</form>
<a href="/">Back</a>
"""

@app.route('/')
def home():
    return home_page

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        uname = request.form['username']
        passwd = request.form['password']

        # convert password to bytes
        password_bytes = passwd.encode('utf-8')

        # hash password with salt
        hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

        # store in our "database"
        users[uname] = hashed

        print("\n[DEBUG INFO]")
        print("Username:", uname)
        print("Original Password:", passwd)
        print("Hashed Password:", hashed)

        flash("Registration Successful!")
        return redirect(url_for('login'))
    return render_template_string(register_page)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        passwd = request.form['password']

        if uname not in users:
            flash("User not found!")
            return redirect(url_for('login'))

        hashed = users[uname]
        password_bytes = passwd.encode('utf-8')

        # check password
        if bcrypt.checkpw(password_bytes, hashed):
            return f"<h3>Welcome {uname}! Login Successful ✅</h3>"
        else:
            return "<h3>Invalid Password ❌</h3>"
    return render_template_string(login_page)

if __name__ == "__main__":
    app.run(debug=True)
