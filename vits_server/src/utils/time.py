from datetime import datetime


def current_timestamp(formate_string: str = None) -> str:
    formate_string = formate_string if formate_string else "%Y%m%d%H%M%S"
    stamp = datetime.strftime(datetime.now(), formate_string)
    return stamp
