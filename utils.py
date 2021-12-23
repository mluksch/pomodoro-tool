def mins_to_sec(mins):
    return mins * 60


def number_to_2digits(x):
    return f"0{x}" if x < 10 else x


def get_mins(time_in_sec):
    return time_in_sec // 60


def get_secs(time_in_sec):
    return time_in_sec % 60


def timer_text(secs):
    return f"{number_to_2digits(get_mins(secs))}:{number_to_2digits(get_secs(secs))}"
