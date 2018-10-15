import datetime

# import flask application
from flask import current_app

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.inspection import inspect


class Serializer(object):

    def serialize(self):
        output = dict()
        for c in inspect(self).attrs.keys():
            if c not in getattr(self, '__exclude__'):
                if isinstance(getattr(self, c), datetime.time):
                    output[c] = getattr(self, c).isoformat()
                elif isinstance(getattr(self, c), db.Model):
                    output[c] = getattr(self, c).serialize()
                else:
                    output[c] = getattr(self, c)

        return output
        # return {c: getattr(self, c).isoformat() if isinstance(getattr(self, c), datetime.time) else getattr(self, c)
        #         for c in inspect(self).attrs.keys() if c not in getattr(self, '__exclude__')}

    @staticmethod
    def serialize_list(model_list):
        return [model_obj.serialize() for model_obj in model_list]


with current_app.app_context():
    # Define database object
    db = SQLAlchemy(current_app)

    class Abstract(db.Model, Serializer):
        __abstract__ = True
        __exclude__ = ['id']

        id = db.Column(db.Integer, primary_key=True)
        date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
        date_updated = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


    class Interviewer(Abstract):
        first_name = db.Column(db.String(255), nullable=False)
        last_name = db.Column(db.String(255), nullable=False)
        email = db.Column(db.String(200), unique=True, nullable=False)

        def __repr__(self):
            return '<Interviewer: %r %r>' % (self.first_name, self.last_name)


    class Candidate(Abstract):
        first_name = db.Column(db.String(255), nullable=False)
        last_name = db.Column(db.String(255), nullable=False)
        email = db.Column(db.String(200), unique=True, nullable=False)

        def __repr__(self):
            return '<Candidate: %r %r>' % (self.first_name, self.last_name)


    class AvailabilitySlot(Abstract):
        # __exclude__ = ['interviewer']
        interviewer_id = db.Column(db.Integer, db.ForeignKey('interviewer.id'), nullable=False)
        interviewer = db.relationship(Interviewer)

        scheduled_date = db.Column(db.Date, nullable=False)
        start_time = db.Column(db.Time, nullable=False)
        end_time = db.Column(db.Time, nullable=False)
        is_booked = db.Column(db.Boolean, default=False)


    class RequestedSlot(Abstract):
        candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)
        scheduled_date = db.Column(db.Date, nullable=False)
        start_time = db.Column(db.Time, nullable=False)
        end_time = db.Column(db.Time, nullable=False)
        is_booked = db.Column(db.Boolean, default=False)