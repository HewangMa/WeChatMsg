from config import *

from app.log import logger
from app.DataBase import msg
from typing import Tuple
from Conversation import Conversation
from datetime import datetime, date


class Waken:
    def __init__(self) -> None:
        self.beauty = "-"*20
        self.bias = 6

    def __get_and_parse_chat_msg(self, time_range):
        content = msg.Msg().get_messages(WAKEN_USERNAME, time_range)
        ret = []
        for one_msg in content:
            sender = "多肉" if one_msg[4] == 0 else "橙子"
            one_msg_ = one_msg[7]
            if one_msg_.startswith('<') or len(one_msg_) < 1:
                continue
            ret.append(f"{sender}: {one_msg_}")
        return ret

    def __waken_one_para(self, para):
        with open(os.path.join(PROMPT_ROOT, "waken_prompt.txt"), 'r', encoding='utf-8') as file:
            msg = file.read()
        msg = msg.replace("{records}", para)
        response = Conversation().get_response_from_llm(question=msg)
        return response

    def waken_one_day(self, YEAR, MONTH, DAY):
        start_time = f"{str(YEAR)}-{str(MONTH)}-{str(DAY)} {HOUR_TIME}"
        end_time = f"{str(YEAR)}-{str(MONTH)}-{str(DAY+1)} {HOUR_TIME}"
        time_range = (start_time, end_time)
        msg_in_one_day = self.__get_and_parse_chat_msg(time_range)
        msg_cnt = len(msg_in_one_day)
        if msg_cnt < 1:
            logger.info(f"None msg in {time_range}~~")
            return
        # 根据总量划分waken次数，并分段（前后来个bias）进行
        whole_msg_in_one_day = "\n".join(msg_in_one_day)
        token_len = token_len_of(whole_msg_in_one_day)
        part_num = token_len // 2000 + 1
        part_msg_cnt = msg_cnt // part_num
        
        for p_idx in range(part_num):
            start_idx = p_idx*part_msg_cnt
            if start_idx > 0:
                start_idx -= self.bias
            end_idx = (p_idx+1)*part_msg_cnt
            if end_idx < msg_cnt-1:
                end_idx += self.bias
            logger.info(f"Trying with start = {start_idx}, end = {end_idx}, msg_cnt = {msg_cnt}")

            para = msg_in_one_day[start_idx:end_idx+1]
            # 分出段之后 去除重复sender
            for i in range(len(para)-1, -1, -1):
                if i > 0 and para[i][0] == para[i-1][0]:
                    para[i] = "    " + para[i][3:]
            logger.info('\n'.join(para))
            one_waken = self.__waken_one_para("\n".join(para))
            logger.info(one_waken)
            break

    def __exact_and_write(self, response, YEAR, MONTH, DAY):
        header = f"{str(YEAR)}-{str(MONTH)}-{str(DAY)}: "
        paras = response.split("{{split}}")
        to_write = ['\n', header]+[self.beauty +'\n' + p for p in paras if len(p) > 2]
        file_name = f"{str(YEAR)}-{str(MONTH)}.txt"
        file_path = os.path.join(WAKEN_RES_ROOT, file_name)
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write('\n'.join(to_write))
        logger.info(f"Successfully wrote records to {file_path}")


if __name__ == "__main__":
    day_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    YEAR = 2023
    MONTH = 2
    DAY = 1
    Waken().waken_one_day(YEAR, MONTH, DAY)
    # for DAY in range(1, day_in_month[MONTH-1]+1):
    #     Waken().waken_one_day(YEAR, MONTH, DAY)
