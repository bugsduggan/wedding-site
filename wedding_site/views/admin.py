from datetime import date

from flask import Blueprint, render_template, abort

from wedding_site.models import *
from wedding_site.models import constants
from wedding_site.forms import AddUserForm, EditNameForm
from wedding_site.forms import GenderForm, GroupForm
from wedding_site.forms import DietaryRequirementsForm
from wedding_site.forms import AddTaskForm
from wedding_site.utils import admin_required


admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.context_processor
def inject_constants():
    return dict(constants=constants)


@admin.route('/')
@admin_required
def dashboard():
    invitations = Invitation.query.filter(Invitation.status != constants.NOT_INVITED).all()
    invitations = sorted(invitations, key=lambda inv: inv.owner.last_name)
    add_user_form = AddUserForm()

    total_users = 0
    total_confirmed = 0
    total_not_responded = 0
    total_declined = 0
    for invitation in invitations:
        for user in invitation.users:
            total_users = total_users + 1
            if user.response_status == constants.CONFIRMED:
                total_confirmed = total_confirmed + 1
            elif user.response_status == constants.NOT_RESPONDED:
                total_not_responded = total_not_responded + 1
            elif user.response_status == constants.DECLINED:
                total_declined = total_declined + 1

    return render_template('dashboard.html',
                           invitations=invitations,
                           total_users=total_users,
                           total_confirmed=total_confirmed,
                           total_not_responded=total_not_responded,
                           total_declined=total_declined,
                           add_user_form=add_user_form)


@admin.route('/todos')
@admin_required
def todos():
    todos = Todo.query.all()
    add_task_form = AddTaskForm()
    return render_template('todos.html', todos=todos,
                           add_task_form=add_task_form)


@admin.route('/group/<string:group_name>')
@admin_required
def group(group_name):
    group = Group.query.filter_by(group_name=group_name).first()
    if not group:
        abort(404)

    return render_template('group.html', group=group)


@admin.route('/users')
@admin_required
def users():
    users = User.query.order_by(User.last_name).all()
    return render_template('users.html', users=users)


@admin.route('/user/<int:uid>')
@admin_required
def user(uid):
    user = User.query.filter_by(uid=uid).first()
    if not user:
        abort(404)

    edit_name_form = EditNameForm()
    edit_name_form.first_name.data = user.first_name
    edit_name_form.last_name.data = user.last_name

    gender_form = GenderForm()
    gender_form.gender.data = user.gender

    group_form = GroupForm()
    group_choices = list()
    for group in Group.query.order_by(Group.group_name).all():
        group_choices.append((group.gid, group.group_display_name))
    group_choices.append((-1, 'New group'))
    group_form.group.choices = group_choices

    dietary_requirements_form = DietaryRequirementsForm()
    dietary_requirements_form.dietary_requirements.data = user.dietary_requirements

    return render_template('user.html', user=user,
                           edit_name_form=edit_name_form,
                           gender_form=gender_form,
                           group_form=group_form,
                           dietary_requirements_form=dietary_requirements_form)
