import re
import requests
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# Function to check if the email is valid
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# Function to check if the password is valid
def is_valid_password(password):
    return len(password) == 6 and re.search(r"[\W_]", password)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if is_valid_email(username) and is_valid_password(password):
            return redirect(url_for('index'))
        else:
            error = "Invalid email or password format. Please try again."
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/logout', methods=['POST'])
def logout():
    return redirect(url_for('login'))

# Webhook endpoint for GitHub push events
@app.route('/github-webhook', methods=['POST'])
def github_webhook():
    payload = request.get_json()

    # Optional: Log payload or specific fields for debugging
    print("Received webhook:", payload)

    if payload and payload.get('ref') == 'refs/heads/main':
        trigger_jenkins_jobs()
        return jsonify({"message": "Jenkins jobs triggered"}), 200
    return jsonify({"message": "No action taken"}), 200

# Trigger Jenkins jobs
def trigger_jenkins_jobs():
    jenkins_url_1 = 'http://localhost:8080/job/job-one/build'
    jenkins_url_2 = 'http://localhost:8080/job/job-two/build'
    jenkins_user = 'karina'
    jenkins_token = '112e5276b5bafcfb06adaac0087523726f'
    auth = (jenkins_user, jenkins_token)

    try:
        res1 = requests.post(jenkins_url_1, auth=auth)
        res2 = requests.post(jenkins_url_2, auth=auth)
        print(f"Triggered job one: {res1.status_code}, job two: {res2.status_code}")
    except Exception as e:
        print("Error triggering Jenkins jobs:", e)

if __name__ == "__main__":
    app.run(debug=True)
