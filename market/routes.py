import time

from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, login_required, logout_user, current_user

from market import app, db
from market.forms import LoginForm, RegisterForm, AddForm
from market.models import Item, User


@app.route('/')
def home_page():
    return render_template('home.html')


@app.route('/achievement', methods=['GET', 'POST'])
def achievement_page():
    form = AddForm()
    if request.method == "POST":
        if form.validate_on_submit():
            t = time.localtime()
            d_o_a_to_save = f"{t.tm_mday}/{t.tm_mon}/{t.tm_year}"
            d_o_d_to_save = f"{form.date_of_do_day.data}/{form.date_of_do_month.data}/{form.date_of_do_day.data}"
            link_to_save = f"https://{form.link.data}"
            achievement_to_add = Item(name=form.name.data,
                                      value=form.value.data,
                                      participants=form.value.data,
                                      school_name=form.school_name.data,
                                      category=form.category.data,
                                      date_of_do=d_o_d_to_save,
                                      description=form.description.data if form.description.data != "" else None,
                                      link=link_to_save if form.link.data != "" else None,
                                      date_of_add=d_o_a_to_save,
                                      owner=current_user.username)
            db.session.add(achievement_to_add)
            db.session.commit()
            flash(f"Rekord pomyślnie utowżono! Nazwa to: {achievement_to_add.name}",
                  category='success')
            return redirect(url_for('achievement_page'))

        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(f'There was an error with creating a user: {err_msg}', category='danger')
        return redirect(url_for('achievement_page'))

    if request.method == "GET":
        items = Item.query.all()
        mail = "biuro.szachy.online@gmail.com"
        return render_template('achievement.html', items=items, mail=mail, current_user=current_user, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(
            username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Zostałeś pomyślnie zalogowany do konta "{attempted_user.username}"',
                  category='success')
            return redirect(url_for('achievement_page'))
        else:
            flash('Nazwa lub hasło użytkownika niezgadza się! Proszę spróbuj ponownie.',
                  category='danger')

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
@login_required
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('achievement_page'))
    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("Zostałeś wylogowany", category='info')
    return redirect(url_for("achievement_page"))
