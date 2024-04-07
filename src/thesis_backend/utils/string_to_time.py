from datetime import datetime


def string_to_time(time_str: str) -> float:
    if len(time_str) == 7:  # Format: '0:00:23'
        time_obj = datetime.strptime(time_str, "%H:%M:%S")
    elif len(time_str) in [9, 10]:  # Format: '0:00:32.36' or '0:00:32.3'
        time_obj = datetime.strptime(time_str, "%H:%M:%S.%f")
    else:
        raise ValueError("Invalid time format")
    total_seconds = (time_obj.hour * 3600) + (time_obj.minute * 60) + time_obj.second + (time_obj.microsecond / 1e6)
    return total_seconds
