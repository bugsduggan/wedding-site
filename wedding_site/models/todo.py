from datetime import date

from wedding_site import db


class Todo(db.Model):
    __tablename__ = 'todos'

    tid = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1024))
    due_date = db.Column(db.Date)
    done = db.Column(db.Boolean, default=False)

    @property
    def overdue(self):
        if self.due_date:
            return self.due_date < date.today()
        return False

    def __repr__(self):
        return '<Todo %s...>' % self.content[16:]
