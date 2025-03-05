import os
import sys
import jieba


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
