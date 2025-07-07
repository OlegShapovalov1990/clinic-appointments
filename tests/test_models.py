from datetime import datetime, timedelta

from app.models import Appointment


def test_calculate_end_time():
    start_time = datetime(2023, 1, 1, 10, 0)
    end_time = Appointment.calculate_end_time(start_time)
    assert end_time == datetime(2023, 1, 1, 10, 30)

    end_time_custom = Appointment.calculate_end_time(start_time, duration=45)
    assert end_time_custom == datetime(2023, 1, 1, 10, 45)
