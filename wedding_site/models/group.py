from sqlalchemy.ext.hybrid import hybrid_property

from wedding_site import db


group_link_table = db.Table('group_link',
                            db.Column('uid', db.Integer,
                                      db.ForeignKey('users.uid'),
                                      nullable=False),
                            db.Column('gid', db.Integer,
                                      db.ForeignKey('groups.gid'),
                                      nullable=False),
                            db.PrimaryKeyConstraint('uid', 'gid'))


class Group(db.Model):
    __tablename__ = 'groups'

    gid = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(32), index=True, unique=True,
                           nullable=False)
    users = db.relationship('User', secondary=group_link_table,
                            backref='groups')
    special = db.Column(db.Boolean, default=False)

    @hybrid_property
    def group_display_name(self):
        return self.group_name.replace('_', ' ').capitalize()

    def __repr__(self):
        return '<Group %s>' % self.group_name
