import os
import sys


sys.path.append("D:\Projects\WeChatMsg")
from app.log import logger
from app.DataBase import msg
from typing import Tuple
from Conversation import Conversation
from datetime import datetime, date



# waken 参数
WAKEN_USERNAME = "wxid_4l0w26l64zj022"
PROMPT_ROOT = "./app/waken/prompts"
HOUR_TIME = '04:00:00'



class Waken:
    def __init__(self) -> None:
        pass

    def get_and_parse_chat_msg(self, time_range):
        content = msg.Msg().get_messages(WAKEN_USERNAME, time_range)
        ret = []
        for one_msg in content:
            sender = "多肉" if one_msg[4] == 0 else "橙子"
            one_msg_ = one_msg[7]
            if one_msg_.startswith('<') or len(one_msg_) < 1:
                continue
            ret.append(f"{sender}: {one_msg_}")
        return ret

    def waken_between(self, time_range: Tuple[int | float | str | date, int | float | str | date] = None,):
        msg_in_one_day = self.get_and_parse_chat_msg(time_range)
        whole_msg_in_one_day = "\n".join(msg_in_one_day)

        with open(os.path.join(PROMPT_ROOT, "waken_prompt.txt"), 'r', encoding='utf-8') as file:
            msg = file.read()
        msg = msg.replace("{records}", whole_msg_in_one_day)
        logger.info(msg)
        # exit()
        response = Conversation().get_response_from_llm(question=msg)
        logger.info(response)


if __name__ == "__main__":
    Waken().waken_between(time_range=(
        f"2023-5-4 {HOUR_TIME}", f"2023-5-5 {HOUR_TIME}"))
