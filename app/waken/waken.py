from config import *

from app.log import logger
from app.DataBase import msg
from typing import Tuple
from Conversation import Conversation
from datetime import datetime, date


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
        for i in range(len(ret)-1, -1, -1):
            if i > 0 and ret[i][0] == ret[i-1][0]:
                ret[i] = "    " + ret[i][3:]
        return ret

    def waken_between(self, time_range: Tuple[int | float | str | date, int | float | str | date] = None,):
        msg_in_one_day = self.get_and_parse_chat_msg(time_range)
        whole_msg_in_one_day = "\n".join(msg_in_one_day)

        with open(os.path.join(PROMPT_ROOT, "waken_prompt.txt"), 'r', encoding='utf-8') as file:
            msg = file.read()
        msg = msg.replace("{records}", whole_msg_in_one_day)
        logger.info(msg)
        response = Conversation().get_response_from_llm(question=msg)
        logger.info(response)


if __name__ == "__main__":
    YEAR = 2023
    MONTH = 5
    DAY = 3
    time_range = (f"{str(YEAR)}-{str(MONTH)}-{str(DAY)} {HOUR_TIME}",
                  f"{str(YEAR)}-{str(MONTH)}-{str(DAY+1)} {HOUR_TIME}")
    Waken().waken_between(time_range)
