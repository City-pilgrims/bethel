import datetime
from django import template
from django.utils.timezone import now

register = template.Library()


@register.filter
def format_date(value):
    """7일 이내: 'x일 전', 7일 이후: 'MM-DD'"""
    if not isinstance(value, (datetime.date, datetime.datetime)):  # 날짜 타입 확인
        return value

    today = now().date()  # 현재 날짜 (datetime.date)

    if isinstance(value, datetime.datetime):
        value = value.date()  # datetime.datetime → datetime.date 변환

    delta = today - value

    if delta.days == 0:
        return "오늘"
    elif delta.days == 1:
        return "어제"
    elif delta.days < 7:
        return f"{delta.days}일 전"
    else:
        return value.strftime("%m월 %d일")  # 'MM-DD' 형식으로 변환