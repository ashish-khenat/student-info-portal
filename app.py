from flask import Flask, render_template, request, redirect, url_for, session, flash
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a strong secret key

data_file = 'MOCK_DATA.csv'  # Path to your CSV file

# Ensure the CSV file exists
if not os.path.exists(data_file):
    df = pd.DataFrame(columns=['id', 'first_name', 'last_name', 'gender', 'picture', 'contact_No', 'username', 'password'])
    df.to_csv(data_file, index=False)

@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    df = pd.read_csv(data_file)
    students = df[['id', 'first_name', 'last_name', 'gender', 'picture', 'contact_No']].to_dict(orient='records')
    return render_template('index.html', students=students)

@app.route('/students')
def students():
    if 'username' not in session:
        return redirect(url_for('login'))
    df = pd.read_csv(data_file)
    students = df[['id', 'first_name', 'last_name', 'gender', 'picture', 'contact_No']].to_dict(orient='records')
    return render_template('student.html', students=students)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        gender = request.form.get('gender')
        contact_no = request.form.get('contact_no')
        username = request.form.get('username')
        password = request.form.get('password')
        
        df = pd.read_csv(data_file)

        # Check if the username already exists
        if df[df['username'] == username].empty:
            new_user = pd.DataFrame([[len(df)+1, first_name, last_name, gender, '', contact_no, username, password]], 
                                     columns=['id', 'first_name', 'last_name', 'gender', 'picture', 'contact_No', 'username', 'password'])
            df = pd.concat([df, new_user], ignore_index=True)
            df.to_csv(data_file, index=False)
            flash('Signup successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username already exists. Please choose a different one.', 'error')
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username:
            flash('Username is required.', 'error')
            return redirect(url_for('login'))

        df = pd.read_csv(data_file)
        user = df[(df['username'] == username) & (df['password'] == password)]

        if not user.empty:
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("Logged out successfully.", "success")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
