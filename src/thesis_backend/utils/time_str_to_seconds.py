from datetime import datetime


def time_str_to_seconds(time_str: str) -> float:
    if len(time_str) == 7:  # Format: '0:00:23'
        time_obj = datetime.strptime(time_str, "%H:%M:%S")
    elif len(time_str) > 8:  # Format: '0:00:32.36' or '0:00:32.3' or '0:00:32.3666667'
        if len(time_str) > 10:
            time_str = time_str[:10]
        time_obj = datetime.strptime(time_str, "%H:%M:%S.%f")
    else:
        print(f"Invalid time format: {time_str}")
        raise ValueError("Invalid time format")
    total_seconds = (time_obj.hour * 3600) + (time_obj.minute * 60) + time_obj.second + (time_obj.microsecond / 1e6)
    return total_seconds
