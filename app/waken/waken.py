from configAndUtils import *

from app.log import logger
from app.DataBase import msg
from typing import Tuple
from Conversation import Conversation


class Waken:
    def __init__(self, date_str) -> None:
        '''
        Waken 接受一个如 %Y-%m-%d %H:%M:%S 格式的开始日期
        不要提供别的类型的参数
        '''
        self.fmt = "%Y-%m-%d %H:%M:%S"
        self.day = datetime.strptime(date_str, self.fmt)
        self.next_day = self.day + timedelta(days=1)
        self.time_range = (date_str, self.next_day.strftime(
            "%Y-%m-%d") + " " + HOUR_TIME)
        self.file_name = self.day.strftime("%Y-%m")+".txt"
        self.file_path = os.path.join(WAKEN_RES_ROOT, self.file_name)
        # 创建文件
        with open(self.file_path, 'a', encoding="utf-8") as _:
            pass
        self.header = self.day.strftime("%Y-%m-%d")
        self.beauty = "-"*20
        self.bias = 6

    def waken_one_day(self):
        # 如果这个文件已经写过了就跳过
        with open(self.file_path, 'r', encoding="utf-8") as file:
            stock = file.read()
            if self.header in stock:
                logger.info(f"Jumping waking {self.day}")
                return
        msg_one_day = self.__parse_chat_msg()
        msg_cnt = len(msg_one_day)
        if msg_cnt < 1:
            logger.info(f"None msg in {self.time_range}~~")
            return
        # 根据总量划分waken次数，并分段（前后来个bias）进行
        msg_one_day_str = "\n".join(msg_one_day)
        token_len = token_len_of(msg_one_day_str)
        part_num = token_len // 2000 + 1
        logger.info(
            f"Records of {self.day} is separated to {part_num} paragraphs")
        part_msg_cnt = msg_cnt // part_num

        waken_one_day = []
        for p_idx in range(part_num):
            start_idx = p_idx*part_msg_cnt
            if start_idx > 0:
                start_idx -= self.bias
            end_idx = (p_idx+1)*part_msg_cnt
            if end_idx < msg_cnt-1:
                end_idx += self.bias
            logger.info(
                f"Waking between [{start_idx}, {end_idx}], total having {msg_cnt} messages")

            para = msg_one_day[start_idx:end_idx+1]
            # 分出段之后 去除重复sender
            for i in range(len(para)-1, -1, -1):
                if i > 0 and para[i][0] == para[i-1][0]:
                    para[i] = "    " + para[i][3:]
            waken_one_para = self.__waken_one_para("\n".join(para))
            waken_one_day.append(waken_one_para)

        self.__exact_and_write('\n'.join(waken_one_day))

    def __parse_chat_msg(self):
        content = msg.Msg().get_messages(WAKEN_USERNAME, self.time_range)
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

    def __exact_and_write(self, waken_one_day):
        paras = waken_one_day.split("{{split}}")
        to_write = ['\n', self.header] + \
            [self.beauty + '\n' + p for p in paras if len(p) >= 5]
        with open(self.file_path, 'a', encoding='utf-8') as file:
            file.write('\n'.join(to_write))
        logger.info(
            f"Successfully wrote waken_res of {self.day} to {self.file_path}")


if __name__ == "__main__":
    YEAR = 2025
    # MONTH = 4
    # DAY = 1
    # Waken().waken_one_day(YEAR, MONTH, DAY)
    for MONTH in range(1, 13):
        for DAY in range(1, days_in_month(YEAR, MONTH)+1):
            day_str = f"{str(YEAR)}-{str(MONTH)}-{str(DAY)} {HOUR_TIME}"
            Waken(day_str).waken_one_day()
