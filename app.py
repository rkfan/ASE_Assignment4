#!/usr/bin/env python

from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps

# Create application object
app = Flask(__name__)

# VERY BAD. FIX THIS LATER, need random key generator. Also separate config file...
app.secret_key = "secret key"	# need secret key for sessions to work properly

# Login required
def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('Login required.')
			return redirect(url_for('login'))
	return wrap

@app.route('/')
@login_required
def home():
    return render_template('index.html')

@app.route('/welcome')
def welcome():
    return render_template("welcome.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		# admin, admin for now....
		if request.form['username'] != 'admin' or request.form['password'] != 'admin':
			error = 'Invalid credentials. Please try again.'
		else:
			session['logged_in'] = True
			flash('Logged in')
			return redirect(url_for('home'))	# Redirect to home

	return render_template('login.html', error=error)

# TODO link the logout to the logout button?
@app.route('/logout')
def logout():
	session.pop('logged_in', None)	# Pops the value of true for logged in
	flash('Logged out')
	return redirect(url_for('welcome'))


if __name__ == '__main__':
    app.run(debug=True)