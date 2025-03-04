from config import *

from app.log import logger
from app.DataBase import msg
from typing import Tuple
from Conversation import Conversation
from datetime import datetime, date


class Waken:
    def __init__(self) -> None:
        self.beauty = "-"*20

    def __get_and_parse_chat_msg(self, time_range):
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

    def waken_one_day(self, YEAR, MONTH, DAY):
        time_range = (f"{str(YEAR)}-{str(MONTH)}-{str(DAY)} {HOUR_TIME}",
                      f"{str(YEAR)}-{str(MONTH)}-{str(DAY+1)} {HOUR_TIME}")
        msg_in_one_day = self.__get_and_parse_chat_msg(time_range)
        if msg_in_one_day is None:
            return
        whole_msg_in_one_day = "\n".join(msg_in_one_day)
        with open(os.path.join(PROMPT_ROOT, "waken_prompt.txt"), 'r', encoding='utf-8') as file:
            msg = file.read()
        msg = msg.replace("{records}", whole_msg_in_one_day)
        token_len = token_len_of(msg)
        if token_len > 4000:
            logger.info("Records are more than 4000, please write manually")
            return
        response = Conversation().get_response_from_llm(question=msg)
        self.__exact_and_write(response, YEAR, MONTH, DAY)

    def __exact_and_write(self, response, YEAR, MONTH, DAY):
        header = f"{str(YEAR)}-{str(MONTH)}-{str(DAY)}: "
        paras = response.split("{{split}}")
        to_write = ['\n', header]+[self.beauty +
                                   '\n' + p for p in paras if len(p) > 2]
        file_name = f"{str(YEAR)}-{str(MONTH)}.txt"
        file_path = os.path.join(WAKEN_RES_ROOT, file_name)
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write('\n'.join(to_write))
        logger.info(f"Successfully wrote records to {file_path}")


if __name__ == "__main__":
    day_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    YEAR = 2023
    MONTH = 3
    # DAY = 1
    # Waken().waken_one_day(YEAR, MONTH, DAY)
    for DAY in range(1, day_in_month[MONTH-1]+1):
        Waken().waken_one_day(YEAR, MONTH, DAY)
