import os
import sys
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
print(PROJECT_ROOT)
sys.path.append(PROJECT_ROOT)
WAKEN_ROOT = os.path.join(PROJECT_ROOT,'app','waken')
WAKEN_USERNAME = "wxid_4l0w26l64zj022"
PROMPT_ROOT = os.path.join(WAKEN_ROOT,'prompts')
HOUR_TIME = '04:00:00'