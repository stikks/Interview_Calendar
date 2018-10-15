from flask import jsonify

from app.models import AvailabilitySlot, Interviewer, Candidate, RequestedSlot

from services.common import InvalidUsage


def retrieve(obj_id):
    """
    retrieve interview slots for candidate
    :param obj_id
    :return
    """
    candidate = Candidate.query.get(obj_id)

    if not candidate:
        raise InvalidUsage("candidate not found matching id - %s" % obj_id, status_code=404)

    request_slots = RequestedSlot.query.filter_by(candidate_id=candidate.id).all()

    slot_dates = [c.scheduled_date for c in request_slots]

    availability_slots = AvailabilitySlot.query.filter(AvailabilitySlot.is_booked==False,
                                                       AvailabilitySlot.scheduled_date.in_(slot_dates)).all()

    return jsonify([d.serialize() for d in availability_slots])