import os
import secrets
from flask import Flask, render_template, url_for, flash, redirect, abort
from webapp import app, db, bcrypt 
from webapp.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from webapp.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required



@app.route('/')
@app.route('/home')
def home():
    posts=Post.query.all()
    return render_template('home.html',posts=posts)

@app.route('/about')
def about():
    return render_template('about.html',posts=posts,title='About')

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    #import the regitration form
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created has been created Now you can log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html',title='register',form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    #import the login form
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):   
            login_user(user,remember=form.remember.data)
            flash(f'Login successful.', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Login Unsuccesful. Please check email and password', 'danger')
    return render_template('login.html',title='Login',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    #unique save
    random_hex=secrets.token_hex(8)
    #to get the extension
    _, f_ext=os.path.splitext(form_picture.filename)
    picture_fn=random_hex+f_ext
    picture_path=os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_path)
    return picture_fn

@app.route('/account', methods=['GET','POST'])
#decorater for login required so user cant access this page if not logged in

def account():
    form=UpdateAccountForm()
    form.username.data=current_user.username
    form.email.data=current_user.email
    if form.validate_on_submit():
        if form.picture.data:
            picture_file=save_picture(form.picture.data)
            current_user.image_file=picture_file
        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash('Your account has been updated!','success')
        return redirect(url_for('account'))
    image_file=url_for('static', filename='profile_pics/' + current_user.image_file)
    if current_user.is_authenticated:
        return render_template('account.html',title='Account', image_file=image_file, form=form)
    else:
        #form=LoginForm()
        flash(f'Login before access', 'danger')
        return redirect(url_for('login'))
    return render_template('account.html',title='Account', image_file=image_file, form=form)

@app.route('/new/posts', methods=['GET','POST'])
def new_post():
    if current_user.is_authenticated:
        form=PostForm()
        if form.validate_on_submit():
            post=Post(title=form.title.data, content=form.content.data, author=current_user)
            db.session.add(post)
            db.session.commit()
            flash(f'Your post had been added successfully!' 'success')
            return redirect(url_for('home'))
        return render_template('create_post.html',title='New Post',form=form,legend='Create Post')
    else:
        flash(f'Login before access', 'danger')
        return redirect(url_for('login'))
    return render_template('create_post.html',title='New Post',form=form,legend='Create Post')

@app.route('/new/<int:post_id>', methods=['GET','POST'])
def post(post_id):
    if current_user.is_authenticated:
        post=Post.query.get_or_404(post_id)
        return render_template('post.html', title=post.title, post=post)
    else:
        flash(f'Login before access', 'danger')
        return redirect(url_for('login'))

@app.route('/new/<int:post_id>/update', methods=['GET','POST'])
def update_post(post_id):
    if current_user.is_authenticated:
        post=Post.query.get_or_404(post_id)
        if post.author!=current_user:
            abort(403)

        form=PostForm()
        if form.validate_on_submit():
            flash(f'Your post had been updated successfully!','success')
            post.title=form.title.data
            post.content=form.content.data
            db.session.commit()
            return redirect(url_for('post', post_id=post.id))
        else:
            form.title.data=post.title
            form.content.data=post.content
        return render_template('create_post.html',title='Update Post',form=form,legend='Update Post')
    else:
        flash(f'Login before access', 'danger')
        return redirect(url_for('login'))

@app.route('/new/<int:post_id>/delete', methods=['GET','POST'])
def delete_post(post_id):
    if current_user.is_authenticated:
        post=Post.query.get_or_404(post_id)
        if post.author!=current_user:
            abort(403)
        db.session.delete(post)
        db.session.commit()
        flash(f'Your post had been deleted successfully!','success')
        return redirect(url_for('home'))
        