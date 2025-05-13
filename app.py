import re
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Function to check if the email is valid
def is_valid_email(email):
    # Simple regex for valid email format
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# Function to check if the password is valid
def is_valid_password(password):
    # Password must be 6 characters and contain at least one special character
    return len(password) == 6 and re.search(r"[\W_]", password)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the email and password are valid
        if is_valid_email(username) and is_valid_password(password):
            # Redirect to the index page if valid credentials
            return redirect(url_for('index'))
        else:
            # If invalid, show error on login page
            error = "Invalid email or password format. Please try again."
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/logout', methods=['POST'])
def logout():
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
