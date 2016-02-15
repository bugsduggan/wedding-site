#!/usr/bin/env python2.7

from wedding_site import create_app, db
from wedding_site.models import *
from wedding_site.models.constants import *


app = create_app()
with app.app_context():
    admin_group = Group.query.filter_by(group_name='admins').first()

    user = User(email='tom.leaman@googlemail.com',
                first_name='Tom',
                last_name='Leaman',
                avatar_url='https://lh6.googleusercontent.com/-if5lIePPC6U/AAAAAAAAAAI/AAAAAAAABDw/uFyXz0YSUWM/photo.jpg?sz=50',
                gender='male',
                social_id='110349729940377521067',
                response_status=CONFIRMED)
    invitation = Invitation(owner=user, status=INVITED_BOTH)
    user.groups.append(admin_group)
    db.session.add(user)
    db.session.add(invitation)
    db.session.commit()

    user = User(email='elton.john@example.com',
                first_name='Elton',
                last_name='John',
                avatar_url='/static/images/prototype/elton.jpg',
                gender='male',
                response_status=CONFIRMED)
    invitation = Invitation(owner=user, total_guests=2, status=INVITED_DAY)
    db.session.add(user)
    db.session.add(invitation)
    db.session.commit()

    user = User(email='emma.watson@example.com',
                first_name='Emma',
                last_name='Watson',
                avatar_url='/static/images/prototype/emma.jpg',
                gender='female')
    invitation = Invitation(owner=user, total_guests=2, status=INVITED_EVENING)
    db.session.add(user)
    db.session.add(invitation)
    db.session.commit()

    user = User(email='george.bush@example.com',
                first_name='George',
                last_name='Bush',
                avatar_url='/static/images/prototype/george.jpg',
                gender='jello',
                response_status=DECLINED,
                dietary_requirements='I like jello!')
    invitation.users.append(user)
    db.session.add(user)
    db.session.add(invitation)
    db.session.commit()

    user = User(email='justin.bieber@example.com',
                first_name='Justin',
                last_name='Bieber',
                avatar_url='/static/images/prototype/justin.jpg',
                gender='male',
                response_status=CONFIRMED)
    invitation = Invitation(owner=user, total_guests=5, status=INVITED_BOTH)
    db.session.add(user)
    db.session.add(invitation)
    db.session.commit()

    user = User(email='kate.bush@example.com',
                first_name='Kate',
                last_name='Bush',
                avatar_url='/static/images/prototype/kate.jpg',
                gender='female',
                response_status=CONFIRMED)
    invitation.users.append(user)
    db.session.add(user)
    db.session.add(invitation)
    db.session.commit()

    user = User(email='richard.stallman@example.com',
                first_name='Richard',
                last_name='Stallman',
                avatar_url='/static/images/prototype/richard.jpg',
                gender='male',
                response_status=DECLINED)
    invitation.users.append(user)
    db.session.add(user)
    db.session.add(invitation)
    db.session.commit()

    user = User(email='robert.deniro@example.com',
                first_name='Robert',
                last_name='DeNiro',
                avatar_url='/static/images/prototype/robert.jpg',
                gender='male')
    invitation = Invitation(owner=user, status=NOT_INVITED)
    db.session.add(user)
    db.session.add(invitation)
    db.session.commit()

    user = User(email='stephen.fry@example.com',
                first_name='Stephen',
                last_name='Fry',
                avatar_url='/static/images/prototype/stephen.jpg',
                gender='male')
    invitation = Invitation(owner=user, status=INVITED_BOTH)
    db.session.add(user)
    db.session.add(invitation)
    db.session.commit()

    user = User(email='tony.blair@example.com',
                first_name='Tony',
                last_name='Blair',
                avatar_url='/static/images/prototype/tony.jpg',
                gender='male')
    db.session.add(user)
    db.session.commit()
