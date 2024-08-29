from datetime import datetime


def format_date(date_string: str) -> str:
    truncated_date_string = date_string[:26] + 'Z'
    dt = datetime.strptime(truncated_date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    formatted_date = dt.strftime("%d-%m-%Y %H:%M:%S")
    return formatted_date
