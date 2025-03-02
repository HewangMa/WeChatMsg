import os
import sys



sys.path.append("D:\Projects\WeChatMsg")

from app.log import logger
from app.DataBase import msg
from app.config import PROMPT_ROOT
from typing import Tuple
from Conversation import Conversation
from datetime import datetime, date



class Waken:
    def __init__(self) -> None:
        pass

    def waken_between(self, username_, time_range: Tuple[int | float | str | date, int | float | str | date] = None,):
        content = msg.Msg().get_messages(username_, time_range)
        logger.info(content)
        # with open(os.path.join(PROMPT_ROOT, "waken_prompt.txt"), 'r', encoding='utf-8') as file:
        #     msg = file.read()
        # # logger.info(msg)
        # response = Conversation().get_response_from_llm(question=msg)


if __name__ == "__main__":
    Waken().waken_between("wxid_4l0w26l64zj022", time_range=("2024-12-1 0:0:0", "2024-12-2 0:0:0"))
