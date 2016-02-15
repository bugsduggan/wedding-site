from flask.ext.login import UserMixin, AnonymousUserMixin
from sqlalchemy.ext.hybrid import hybrid_property

from wedding_site import db, lm
from wedding_site.models.constants import *


class AnonymousUser(AnonymousUserMixin):

    def has_group(self, group_name):
        return False

    def is_admin(self):
        return False


lm.anonymous_user = AnonymousUser


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    uid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)

    invitation_iid = db.Column(db.Integer,
                               db.ForeignKey('invitations.iid',
                                             use_alter=True))
    invitation = db.relationship('Invitation', backref='users',
                                 foreign_keys='User.invitation_iid',
                                 post_update=True)
    response_status = db.Column(db.Integer, default=NOT_RESPONDED,
                                nullable=False)

    social_id = db.Column(db.String(64), unique=True, default=None,
                          nullable=True)
    first_name = db.Column(db.String(64), default='')
    last_name = db.Column(db.String(64), default='')
    gender = db.Column(db.String(16), default='')
    avatar_url = db.Column(db.String(120), default='')

    dietary_requirements = db.Column(db.String(1024), default='')

    def get_id(self):
        return unicode(self.uid)

    @hybrid_property
    def full_name(self):
        if self.first_name and self.last_name:
            return '%s %s' % (self.first_name, self.last_name)
        return '[%s]' % self.email

    def __repr__(self):
        return '<User %s>' % self.full_name

    def has_group(self, group_name):
        for group in self.groups:
            if group.group_name == group_name:
                return True
        return False

    def is_admin(self):
        return self.has_group('admins')


@lm.user_loader
def user_loader(uid):
    return User.query.get(int(uid))
