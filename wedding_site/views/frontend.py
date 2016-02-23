from flask import Blueprint, render_template, redirect, url_for
from flask import flash, session, request
from flask.ext.login import login_user, current_user, logout_user
from flask.ext.login import login_required

from wedding_site import db
from wedding_site.auth import OAuthSignIn
from wedding_site.forms import AddGuestForm
from wedding_site.forms import DietaryRequirementsForm
from wedding_site.models import *
from wedding_site.models import constants


frontend = Blueprint('frontend', __name__)


@frontend.context_processor
def inject_constants():
    return dict(constants=constants)


@frontend.route('/')
def index():
    return render_template('index.html')


@frontend.route('/countdown')
def countdown():
    return render_template('countdown.html')


@frontend.route('/me')
@login_required
def user():
    user = current_user
    if user.invitation is None or user.invitation.status == constants.NOT_INVITED:
        return render_template('not_invited.html')
    else:
        dietary_requirements_form = DietaryRequirementsForm()
        dietary_requirements_form.dietary_requirements.data = user.dietary_requirements
        add_guest_form = AddGuestForm()
        return render_template('rsvp.html', user=user,
                               dietary_requirements_form=dietary_requirements_form,
                               add_guest_form=add_guest_form)


@frontend.route('/update_dietary_requirements', methods=['POST'])
def update_dietary_requirements():
    user = current_user
    form = DietaryRequirementsForm(request.form)
    if not form.validate():
        flash('Something went wrong', 'danger')
        return redirect(url_for('.user'))
    user.dietary_requirements = form.dietary_requirements.data
    db.session.add(user)
    db.session.commit()
    flash('Your dietary requirements have been updated successfully', 'success')
    return redirect(url_for('.user'))


@frontend.route('/delete_guest/<int:uid>')
def delete_guest(uid):
    user = current_user
    if user.invitation.owner != user:
        flash('Only the invitation\'s owner can do that!', 'danger')
        return redirect(url_for('.user'))
    guest = User.query.filter_by(uid=uid).first()
    if not guest:
        flash('Something went wrong', 'danger')
        return redirect(url_for('.user'))

    guest.invitation = None
    guest.response_status = constants.NOT_RESPONDED
    db.session.add(guest)
    db.session.commit()

    flash('%s deleted' % guest.full_name, 'success')
    return redirect(url_for('.user'))


@frontend.route('/add_guest', methods=['POST'])
def add_guest():
    user = current_user
    if user.invitation.owner != user:
        flash('Only the invitation\'s owner can do that!', 'danger')
        return redirect(url_for('.user'))
    form = AddGuestForm(request.form)
    if not form.validate():
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                ))
        flash('Something went wrong', 'danger')
        return redirect(url_for('.user'))

    email = form.email.data
    first_name = form.first_name.data
    last_name = form.last_name.data
    guest = User.query.filter_by(email=email).first()
    if not guest:
        guest = User(email=email)
        if first_name:
            guest.first_name = first_name
        if last_name:
            guest.last_name = last_name
        db.session.add(guest)
        db.session.commit()
    if guest.invitation:
        flash('%s has already been invited' % guest.full_name, 'danger')
        return redirect(url_for('.user'))

    user.invitation.users.append(guest)
    db.session.add(user.invitation)
    db.session.commit()

    flash('%s has been invited' % guest.full_name, 'success')
    return redirect(url_for('.user'))


@frontend.route('/me/decline')
@login_required
def decline_user():
    user = current_user
    if user.response_status != constants.NOT_RESPONDED:
        flash('You\'ve already RSVPd!', 'warning')
        return redirect(url_for('.user'))

    user.response_status = constants.DECLINED
    db.session.add(user)
    db.session.commit()

    flash('We\'ll miss you, but thanks for letting us know!', 'success')
    return redirect(url_for('.user'))


@frontend.route('/me/confirm')
@login_required
def confirm_user():
    user = current_user
    if user.response_status != constants.NOT_RESPONDED:
        flash('You\'ve already RSVPd!', 'warning')
        return redirect(url_for('.user'))

    user.response_status = constants.CONFIRMED
    db.session.add(user)
    db.session.commit()

    flash('We\'re so glad you can come, thanks for letting us know!', 'success')
    return redirect(url_for('.user'))


@frontend.route('/authorize')
def oauth_authorize():
    if not current_user.is_anonymous:
        return redirect(url_for('.index'))
    session['login_next'] = request.args.get('next', None)
    oauth = OAuthSignIn.get_provider('google')
    return oauth.authorize()


@frontend.route('/callback')
def oauth_callback():
    if not current_user.is_anonymous:
        return redirect(url_for('.index'))
    oauth = OAuthSignIn.get_provider('google')
    user_data = oauth.callback()
    if user_data is None:
        flash('Authentication failed', 'danger')
        return redirect(url_for('.index'))

    user = User.query.filter_by(email=user_data['email']).first()
    if not user:
        user = User(
            email=user_data['email'],
            social_id=user_data['social_id'],
            gender=user_data['gender'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            avatar_url=user_data['avatar_url']
        )
        db.session.add(user)
        db.session.commit()
    else:
        user.first_name = user_data['first_name']
        user.last_name = user_data['last_name']
        user.gender = user_data['gender']
        user.social_id = user_data['social_id']
        user.avatar_url = user_data['avatar_url']
        db.session.add(user)
        db.session.commit()
    login_user(user, True)

    login_next = session.get('login_next')
    if login_next is None:
        login_next = url_for('frontend.index')

    flash('Login successful! Hello %s' % user.full_name, 'success')
    return redirect(login_next)


@frontend.route('/logout')
def logout():
    logout_user()
    flash('You are now logged out', 'success')
    return redirect(url_for('.index'))
