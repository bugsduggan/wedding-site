from flask import Blueprint, redirect, render_template, url_for
from flask import flash, abort, request

from wedding_site import db
from wedding_site.models import *
from wedding_site.forms import AddUserForm, EditNameForm
from wedding_site.forms import GenderForm, GroupForm
from wedding_site.forms import DietaryRequirementsForm
from wedding_site.utils import admin_required


api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/delete_invitation/<int:iid>')
@admin_required
def delete_invitation(iid):
    invitation = Invitation.query.filter_by(iid=iid).first()
    if not invitation:
        abort(404)
    for user in invitation.users[:]:
        user.invitation = None
        user.response_status = constants.NOT_RESPONDED
        db.session.add(user)
    db.session.delete(invitation)
    db.session.commit()
    flash('Invitation deleted', 'success')
    return redirect(url_for('admin.dashboard'))


@api.route('/increase_invitation/<int:iid>')
@admin_required
def increase_invitation(iid):
    invitation = Invitation.query.filter_by(iid=iid).first()
    if not invitation:
        abort(404)
    if invitation.owner.is_admin():
        flash('You don\'t need to do that', 'info')
        return redirect(url_for('admin.dashboard'))
    invitation.total_guests = invitation.total_guests + 1
    db.session.add(invitation)
    db.session.commit()
    return redirect(url_for('admin.dashboard'))


@api.route('/decrease_invitation/<int:iid>')
@admin_required
def decrease_invitation(iid):
    invitation = Invitation.query.filter_by(iid=iid).first()
    if not invitation:
        abort(404)

    if len(invitation.users) >= invitation.total_guests:
        flash('Invalid request', 'danger')
        return redirect(url_for('admin.dashboard'))

    invitation.total_guests = invitation.total_guests - 1
    db.session.add(invitation)
    db.session.commit()
    return redirect(url_for('admin.dashboard'))


@api.route('/invitation_day/<int:iid>')
@admin_required
def invitation_day(iid):
    invitation = Invitation.query.filter_by(iid=iid).first()
    if not invitation:
        abort(404)
    invitation.status = constants.INVITED_DAY
    for user in invitation.users:
        user.response_status = constants.NOT_RESPONDED
        db.session.add(user)
    db.session.add(invitation)
    db.session.commit()
    return redirect(url_for('admin.dashboard'))


@api.route('/invitation_evening/<int:iid>')
@admin_required
def invitation_evening(iid):
    invitation = Invitation.query.filter_by(iid=iid).first()
    if not invitation:
        abort(404)
    invitation.status = constants.INVITED_EVENING
    for user in invitation.users:
        user.response_status = constants.NOT_RESPONDED
        db.session.add(user)
    db.session.add(invitation)
    db.session.commit()
    return redirect(url_for('admin.dashboard'))


@api.route('/invitation_both/<int:iid>')
@admin_required
def invitation_both(iid):
    invitation = Invitation.query.filter_by(iid=iid).first()
    if not invitation:
        abort(404)
    invitation.status = constants.INVITED_BOTH
    for user in invitation.users:
        user.response_status = constants.NOT_RESPONDED
        db.session.add(user)
    db.session.add(invitation)
    db.session.commit()
    return redirect(url_for('admin.dashboard'))


@api.route('/add_user', methods=['POST'])
@admin_required
def add_user():
    form = AddUserForm(request.form)
    if not form.validate():
        flash('Something went wrong validating your input', 'danger')
        return redirect(url_for('admin.dashboard'))

    email = form.email.data
    first_name = form.first_name.data
    last_name = form.last_name.data
    invitation_iid = int(form.invitation_iid.data)
    invitation_size = form.invitation_size.data
    invitation_status = form.invitation_status.data

    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email)
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
    if user.invitation:
        flash('The user already has an invitation attached... somewhere', 'danger')
        return redirect(url_for('admin.dashboard'))

    if invitation_iid > 0:
        invitation = Invitation.query.filter_by(iid=invitation_iid).first()
        if not invitation:
            flash('The invitation you\'re trying to attach to cannot be found', 'danger')
            return redirect(url_for('admin.dashboard'))
        if len(invitation.users) >= invitation.total_guests:
            flash('That invitation is already full', 'danger')
            return redirect(url_for('admin.dashboard'))
        invitation.users.append(user)
    else:
        invitation = Invitation(owner=user,
                                status=invitation_status,
                                total_guests=invitation_size)
    
    db.session.add(user)
    db.session.commit()

    flash('%s added' % user.full_name, 'success')
    return redirect(url_for('admin.dashboard'))


@api.route('/delete_user/<int:uid>')
@admin_required
def delete_user(uid):
    user = User.query.filter_by(uid=uid).first()
    if not user:
        abort(404)
    if user.invitation.owner == user and len(user.invitation.users) > 1:
        flash('That invitation still has guests attached', 'danger')
        return redirect(url_for('admin.dashboard'))

    if len(user.invitation.users) == 1:
        db.session.delete(user.invitation)
    user.invitation = None

    user.response_status = constants.NOT_RESPONDED

    db.session.add(user)
    db.session.commit()

    flash('%s deleted' % user.full_name, 'success')
    return redirect(url_for('admin.dashboard'))


@api.route('/confirm_user/<int:uid>')
@admin_required
def confirm_user(uid):
    user = User.query.filter_by(uid=uid).first()
    if not user:
        abort(404)
    user.response_status = constants.CONFIRMED
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('admin.dashboard'))


@api.route('/nullify_user/<int:uid>')
@admin_required
def nullify_user(uid):
    user = User.query.filter_by(uid=uid).first()
    if not user:
        abort(404)
    user.response_status = constants.NOT_RESPONDED
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('admin.dashboard'))


@api.route('/decline_user/<int:uid>')
@admin_required
def decline_user(uid):
    user = User.query.filter_by(uid=uid).first()
    if not user:
        abort(404)
    user.response_status = constants.DECLINED
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('admin.dashboard'))


@api.route('/edit_user_name/<int:uid>', methods=['POST'])
@admin_required
def edit_user_name(uid):
    user = User.query.filter_by(uid=uid).first()
    if not user:
        abort(404)

    form = EditNameForm(request.form)
    if not form.validate():
        flash('Something went wrong validating your input', 'danger')
        return redirect(url_for('admin.user'))

    first_name = form.first_name.data
    last_name = form.last_name.data

    user.first_name = first_name
    user.last_name = last_name

    db.session.add(user)
    db.session.commit()

    return redirect(url_for('admin.user', uid=user.uid))


@api.route('/update_gender/<int:uid>', methods=['POST'])
@admin_required
def update_gender(uid):
    user = User.query.filter_by(uid=uid).first()
    if not user:
        abort(404)

    form = GenderForm(request.form)
    if not form.validate():
        flash('Something went wrong validating your input', 'danger')
        return redirect(url_for('admin.user'))

    gender = form.gender.data
    if gender == 'other':
        user.gender = form.other.data
    else:
        user.gender = gender

    db.session.add(user)
    db.session.commit()

    return redirect(url_for('admin.user', uid=user.uid))


@api.route('/add_group/<int:uid>', methods=['POST'])
@admin_required
def add_group(uid):
    user = User.query.filter_by(uid=uid).first()
    if not user:
        abort(404)

    form = GroupForm(request.form)
    group_choices = list()
    for group in Group.query.order_by(Group.group_name).all():
        group_choices.append((group.gid, group.group_display_name))
    group_choices.append((-1, 'New group'))
    form.group.choices = group_choices
    if not form.validate():
        flash('Something went wrong validating your input', 'danger')
        return redirect(url_for('admin.user'))

    gid = form.group.data
    group_name = form.group_name.data.lower().replace(' ', '_')

    if gid == -1:
        group = Group(group_name=group_name)
    else:
        group = Group.query.filter_by(gid=gid).first()
        if not group:
            flash('Group not found', 'danger')
            return redirect(url_for('admin.user'))

    user.groups.append(group)

    db.session.add(user)
    db.session.commit()

    return redirect(url_for('admin.user', uid=user.uid))


@api.route('/remove_group/<int:uid>/<int:gid>')
@admin_required
def remove_group(uid, gid):
    user = User.query.filter_by(uid=uid).first()
    if not user:
        abort(404)
    group = Group.query.filter_by(gid=gid).first()
    if not group:
        abort(404)

    if group in user.groups:
        user.groups.remove(group)

    db.session.add(user)
    db.session.commit()

    flash('%s removed from %s' % (user.full_name, group.group_display_name),
          'success')
    return redirect(url_for('admin.user', uid=user.uid))


@api.route('/update_dietary_requirements/<int:uid>', methods=['POST'])
@admin_required
def update_dietary_requirements(uid):
    user = User.query.filter_by(uid=uid).first()
    if not user:
        abort(404)

    form = DietaryRequirementsForm(request.form)
    if not form.validate():
        flash('Something went wrong validating your input', 'danger')
        return redirect(url_for('admin.user'))

    dietary_requirements = form.dietary_requirements.data
    user.dietary_requirements = dietary_requirements

    db.session.add(user)
    db.session.commit()

    return redirect(url_for('admin.user', uid=user.uid))


@api.route('/delete_group/<int:gid>')
@admin_required
def delete_group(gid):
    group = Group.query.filter_by(gid=gid).first()
    if not group:
        abort(404)

    db.session.delete(group)
    db.session.commit()

    flash('%s group deleted' % group.group_display_name, 'success')
    return redirect(url_for('admin.dashboard'))
