from auth.models import Flag


def check_flag(flag_name):
    flag_filter = Flag.objects.filter(name=flag_name)
    if flag_filter.exists():
        return flag_filter.first().active
    return False
