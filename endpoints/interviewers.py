from flask import jsonify

import connexion

from app import forms, models, InvalidUsage

from services import common


def all():
    """
    json response of available interviewers
    :return:
    """
    url_params = connexion.request.args
    page = url_params.get('page', 0)
    limit = url_params.get('limit', 20)
    return jsonify({"data": [c.serialize() for c in models.Interviewer.query.offset(page).limit(limit).all()]})


def get(obj_id):
    """
    retrieves interviewer record matching obj_id
    :param obj_id:
    :return:
    """
    interviewer = models.Interviewer.query.get(obj_id)

    if not interviewer:
        raise InvalidUsage("Interviewer not found matching id - %s" % obj_id, status_code=404)

    return jsonify({"data": interviewer.serialize()})


def create(**kwargs):
    """
    creates new interviewer record
    :param kwargs:
    :return:
    """
    request_data = kwargs.get('data')
    form = forms.CreateForm(csrf_enabled=False, obj=request_data)

    if form.validate_on_submit():

        if models.Interviewer.query.filter_by(email=form.email.data).first():
            raise InvalidUsage("Interviewer with email address already - %s exists" % form.email.data, status_code=400)

        interviewer = models.Interviewer()
        form.populate_obj(interviewer)
        models.db.session.add(interviewer)
        models.db.session.commit()
        return jsonify({"message": "Interviewer with id - %s created" % interviewer.id})

    raise InvalidUsage(form.errors, status_code=422)


def delete(obj_id):
    """
    deletes interviewer record matching obj_id
    :param obj_id:
    :return:
    """
    interviewer = models.Interviewer.query.get(obj_id)

    if not interviewer:
        raise InvalidUsage("Interviewer not found matching id - %s" % obj_id, status_code=404)

    models.db.session.delete(interviewer)
    models.db.session.commit()

    return common.success_response("Interviewer successfully deleted", 204)


def update(obj_id, **kwargs):
    """
    updates interviewer record matching obj_id with data in request body
    :param obj_id:
    :param args:
    :param kwargs:
    :return:
    """
    interviewer = models.Interviewer.query.get(obj_id)

    if not interviewer:
        raise InvalidUsage("Interviewer not found matching id - %s" % obj_id, status_code=404)

    request_data = kwargs.get('data')

    form = forms.UpdateForm(csrf_enabled=False, obj=request_data)

    if form.validate_on_submit():
        common.populate_object(interviewer, **request_data)
        models.db.session.add(interviewer)
        models.db.session.commit()
        return common.success_response({"message": "Interviewer with id - %s successfully updated" % interviewer.id}, 201)

    raise InvalidUsage(form.errors, status_code=422)