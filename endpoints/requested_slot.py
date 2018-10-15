from datetime import timedelta

from flask import jsonify
import connexion

from app import forms, models
from services.common import InvalidUsage, success_response


def retrieve(obj_id):
    """
    retrieve request slots matching obj_id
    :param obj_id
    :return
    """
    candidate = models.Candidate.query.get(obj_id)

    if not candidate:
        raise InvalidUsage("Candidate not found matching id - %s" % obj_id, status_code=404)

    url_params = connexion.request.args
    page = url_params.get('page', 0)
    limit = url_params.get('limit', 20)

    slots = models.RequestedSlot.query.filter_by(candidate_id=candidate.id,
                                                 is_booked=False).offset(page).limit(limit).all()

    return [i.serialize() for i in slots]


def create(obj_id, **kwargs):
    """
    creates new candidate request record
    :param obj_id:
    :param kwargs:
    :return:
    """
    candidate = models.Candidate.query.get(obj_id)

    if not candidate:
        raise InvalidUsage("candidate not found matching id - %s" % obj_id, status_code=404)

    request_data = kwargs.get('data')
    form = forms.AvailabilityForm(csrf_enabled=False, obj=request_data)

    if form.validate_on_submit():
        if models.RequestedSlot.query.filter_by(scheduled_date=form.scheduled_date.data,
                                                start_time=form.start_time.data, end_time=form.end_time.data).first():
            raise InvalidUsage("Slot already exists", status_code=400)

        slot = models.RequestedSlot()
        slot.candidate_id = candidate.id
        form.populate_obj(slot)
        models.db.session.add(slot)
        models.db.session.commit()
        return jsonify({"message": "Request slot on date - {} scheduled for {} - "
                                   "{}".format(slot.scheduled_date, slot.start_time, slot.end_time)})

    raise InvalidUsage(form.errors, status_code=422)


def create_range(obj_id, **kwargs):
    """
    creates new candidate request record for date range
    :param obj_id:
    :param kwargs:
    :return:
    """
    candidate = models.Candidate.query.get(obj_id)

    if not candidate:
        raise InvalidUsage("candidate not found matching id - %s" % obj_id, status_code=404)

    request_data = kwargs.get('data')
    form = forms.RangeForm(csrf_enabled=False, obj=request_data)

    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
        period = end_date - start_date

        for i in range(0, period.days+1):
            select_date = start_date + timedelta(days=i)

            if models.RequestedSlot.query.filter_by(scheduled_date=select_date, start_time=form.start_time.data,
                                                    end_time=form.end_time.data).first():
                raise InvalidUsage("Slot already exists", status_code=400)

            slot = models.RequestedSlot()
            slot.candidate_id = candidate.id
            slot.scheduled_date = select_date
            form.populate_obj(slot)
            models.db.session.add(slot)
            models.db.session.commit()
        return jsonify({"message": "Requested slot dates created"})

    raise InvalidUsage(form.errors, status_code=422)


def delete(obj_id):
    """
    deletes request slot record matching obj_id
    :param obj_id:
    :return:
    """
    slot = models.RequestedSlot.query.get(obj_id)

    if not slot:
        raise InvalidUsage("Request slot not found matching id - %s" % obj_id, status_code=404)

    models.db.session.delete(slot)
    models.db.session.commit()

    return success_response("Request slot successfully deleted", 204)
