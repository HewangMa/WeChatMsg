import os
import sys
import jieba
from datetime import datetime, date, timedelta


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(PROJECT_ROOT)
WAKEN_ROOT = os.path.join(PROJECT_ROOT, 'app', 'waken')
WAKEN_RES_ROOT = os.path.join(WAKEN_ROOT, "waken_res")
WAKEN_USERNAME = "wxid_4l0w26l64zj022"
PROMPT_ROOT = os.path.join(WAKEN_ROOT, 'prompts')
HOUR_TIME = '04:00:00'


def tokens(msg):
    return list(jieba.cut(msg))


def token_len_of(msg):
    return len(tokens(msg))


def days_in_month(year: int, month: int) -> int:
    """计算指定年份和月份的天数"""
    if month == 12:
        next_month = datetime(year + 1, 1, 1)
    else:
        next_month = datetime(year, month + 1, 1)
    last_day = next_month - timedelta(days=1)
    return last_day.day
