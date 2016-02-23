#!/usr/bin/env python2.7

import os.path

from wedding_site import create_app, db
from wedding_site.models import *


app = create_app()
SQLALCHEMY_DATABASE_URI = app.config['SQLALCHEMY_DATABASE_URI']


with app.app_context():
    db.create_all()

    admin_group = Group(group_name='admins', special=True)
    db.session.add(admin_group)
    db.session.commit()

    bridal_party_group = Group(group_name='bridal_party', special=True)
    db.session.add(bridal_party_group)
    db.session.commit()

    groomsmen_group = Group(group_name='groomsmen', special=True)
    db.session.add(groomsmen_group)
    db.session.commit()

    best_men_group = Group(group_name='best_men', special=True)
    db.session.add(best_men_group)
    db.session.commit()

    bridesmaid_group = Group(group_name='bridesmaids', special=True)
    db.session.add(bridesmaid_group)
    db.session.commit()

    maid_of_honour_group = Group(group_name='maids_of_honour', special=True)
    db.session.add(maid_of_honour_group)
    db.session.commit()

    parent_group = Group(group_name='parents', special=True)
    db.session.add(parent_group)
    db.session.commit()

    farmhouse_group = Group(group_name='farmhouse_guests', special=True)
    db.session.add(farmhouse_group)
    db.session.commit()

    contractor_group = Group(group_name='contractors', special=True)
    db.session.add(contractor_group)
    db.session.commit()
