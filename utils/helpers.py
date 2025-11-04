from sqlalchemy import func
from models.models import Appointment, db


def get_popular_services():
    """Returns a list of popular services with their appointment counts."""
    popular_services = db.session.query(
        Appointment.service, func.count(Appointment.id)
    ).group_by(Appointment.service).order_by(func.count(Appointment.id).desc()).all()
    return [{'service': service, 'count': count} for service, count in popular_services]

def get_peak_hours():
    """Analyzes appointments and returns data for peak hours."""
    peak_hours = db.session.query(
        func.strftime('%H', Appointment.time), func.count(Appointment.id)
    ).group_by(func.strftime('%H', Appointment.time)).order_by(func.strftime('%H', Appointment.time)).all()
    return {'labels': [hour for hour, _ in peak_hours], 'values': [count for _, count in peak_hours]}
