from datetime import date, datetime

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, BooleanField, TimeField, DateField
from wtforms.validators import Optional, DataRequired, Email, Regexp, ValidationError
from wtforms.fields.html5 import EmailField


class CreateForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])


class UpdateForm(FlaskForm):
    first_name = StringField('First Name', validators=[Optional()])
    last_name = StringField('Last Name', validators=[Optional()])
    email = EmailField("Email", validators=[Optional()])


class AvailabilityForm(FlaskForm):
    scheduled_date = DateField('Scheduled Date', validators=[DataRequired(), Regexp('^[0-9]{4}-[0-9]{2}-[0-9]{2}$',
                                                                                    message='Invalid date format')])
    start_time = TimeField("Start Time", validators=[DataRequired(), Regexp('^[0-9]{2}:[0-9]{2}$',
                                                                            message='Invalid time format')])
    end_time = TimeField("End Time", validators=[DataRequired(), Regexp('^[0-9]{2}:[0-9]{2}$',
                                                                        message='Invalid time format')])

    def validate(self):
        """
        custom validator
        """
        start_time = self.data.get('start_time')
        end_time = self.data.get('end_time')
        scheduled_date = self.data.get('scheduled_date')

        if start_time.minute != 0:
            self.start_time.errors.append("Invalid time format, should be like 02:00")
            return False

        if end_time.minute != 0:
            self.end_time.errors.append("Invalid time format, should be like 02:00")
            return False

        if start_time > end_time:
            self.start_time.errors = self.start_time.errors + ("Invalid time format, start time should be less "
                                                               "than end time",)
            return False

        duration = datetime.combine(date.min, start_time) - datetime.combine(date.min, end_time)
        if duration.total_seconds() > 3600:
            self.start_time.errors = self.start_time.errors + ("Invalid duration, it should be a max of 1 hour",)
            return False

        if scheduled_date < date.today():
            self.scheduled_date.errors = self.scheduled_date.errors + ("Invalid date format, scheduled date should be"
                                                                       " at least today",)
            return False

        return True


class RangeForm(FlaskForm):
    start_time = TimeField("Start Time", validators=[DataRequired(), Regexp('^[0-9]{2}:[0-9]{2}$',
                                                                            message='Invalid time format')])
    end_time = TimeField("End Time", validators=[DataRequired(), Regexp('^[0-9]{2}:[0-9]{2}$',
                                                                        message='Invalid time format')])
    start_date = DateField('Start Date', validators=[DataRequired(), Regexp('^[0-9]{4}-[0-9]{2}-[0-9]{2}$',
                                                                                    message='Invalid date format')])
    end_date = DateField('End Date', validators=[DataRequired(), Regexp('^[0-9]{4}-[0-9]{2}-[0-9]{2}$',
                                                                                    message='Invalid date format')])

    def validate(self):
        """
        custom validator
        """
        start_time = self.data.get('start_time')
        end_time = self.data.get('end_time')

        if start_time.minute != 0:
            self.start_time.errors.append("Invalid time format, should be like 02:00")
            return False

        if end_time.minute != 0:
            self.end_time.errors.append("Invalid time format, should be like 02:00")
            return False

        if start_time > end_time:
            self.start_time.errors = self.start_time.errors + ("Invalid time format, start time should be less "
                                                               "than end time",)
            return False

        start_date = self.data.get('start_date')
        end_date = self.data.get('end_date')

        if start_date > end_date:
            self.start_date.errors = self.start_date.errors + ("Invalid date format, start date should be less "
                                                               "than end date",)
            return False

        if start_date < date.today():
            self.start_date.errors = self.start_date.errors + ("Invalid date format, start date should be at least "
                                                               "today",)
            return False

        duration = datetime.combine(date.min, start_time) - datetime.combine(date.min, end_time)
        if duration.total_seconds() > 3600:
            self.start_time.errors = self.start_time.errors + ("Invalid duration, it should be a max of 1 hour")
            return False

        return True
