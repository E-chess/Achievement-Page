import datetime
import time

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user

from market import app, db
from market.forms import AddForm, LoginForm, RegisterForm
from market.models import Item, User


@app.route("/")
def home_page():
    return render_template("home.html")


@app.route("/achievement", methods=["GET", "POST"])
def achievement_page():
    form = AddForm()
    if request.method == "POST":
        if form.validate_on_submit():
            t = time.localtime()
            d_o_a_to_save = datetime.datetime(int(t.tm_year), int(t.tm_mon),
                                              int(t.tm_mday))
            d_o_d_to_save = datetime.datetime(
                int(form.date_of_do_year.data),
                int(form.date_of_do_month.data),
                int(form.date_of_do_day.data),
            )
            link_to_save = f"https://{form.link.data}"
            achievement_to_add = Item(
                name=form.name.data,
                value=form.value.data,
                participants=form.value.data,
                school_name=form.school_name.data,
                category=form.category.data,
                date_of_do=d_o_d_to_save,
                description=form.description.data
                if form.description.data != "" else None,
                link=link_to_save if form.link.data != "" else None,
                date_of_add=d_o_a_to_save,
                owner=current_user.username,
            )
            db.session.add(achievement_to_add)
            db.session.commit()
            flash(
                f"Rekord pomyślnie utowżono! Nazwa to: {achievement_to_add.name}",
                category="success",
            )
            return redirect(url_for("achievement_page"))

        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(
                    f"There was an error with creating a user: {err_msg}",
                    category="danger",
                )
        return redirect(url_for("achievement_page"))

    if request.method == "GET":
        items = db.session.query(Item).order_by(Item.id)

        mail = "biuro.szachy.online@gmail.com"
        return render_template(
            "achievement.html",
            items=items,
            mail=mail,
            current_user=current_user,
            form=form,
        )


@app.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = (db.session.query(User).filter_by(
            username=form.username.data).first())
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data):
            login_user(attempted_user)
            flash(
                f'Zostałeś pomyślnie zalogowany do konta "{attempted_user.username}"',
                category="success",
            )
            return redirect(url_for("achievement_page"))
        else:
            flash(
                "Nazwa lub hasło użytkownika niezgadza się! Proszę spróbuj ponownie.",
                category="danger",
            )

    return render_template("login.html", form=form)


# noinspection PyArgumentList
@app.route("/register", methods=["GET", "POST"])
# @login_required
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(
            username=form.username.data,
            email_address=form.email_address.data,
            password=form.password1.data,
        )
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(
            f"Account created successfully! You are now logged in as {user_to_create.username}",
            category="success",
        )
        return redirect(url_for("achievement_page"))
    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f"There was an error with creating a user: {err_msg}",
                  category="danger")

    return render_template("register.html", form=form)


@app.route("/logout")
def logout_page():
    logout_user()
    flash("Zostałeś wylogowany", category="info")
    return redirect(url_for("achievement_page"))
