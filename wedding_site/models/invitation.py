from wedding_site import db
from wedding_site.models.constants import *


class Invitation(db.Model):
    __tablename__ = 'invitations'

    iid = db.Column(db.Integer, primary_key=True)
    owner_uid = db.Column(db.Integer, db.ForeignKey('users.uid'),
                          nullable=False)
    owner = db.relationship('User', foreign_keys='Invitation.owner_uid')
    total_guests = db.Column(db.Integer, default=1)
    status = db.Column(db.Integer, default=NOT_INVITED)

    def __init__(self, owner, total_guests=1, status=NOT_INVITED, users=None):
        self.owner = owner
        self.total_guests = total_guests
        self.status = status
        self.users = users or []

        db.session.add(self)
        db.session.commit()

        if self.owner not in self.users:
            self.users.append(self.owner)

    def __repr__(self):
        return '<Invitation #%d>' % self.iid
