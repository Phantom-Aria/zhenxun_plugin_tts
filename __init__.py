from typing import Tuple, Any
from utils.http_utils import AsyncHttpx
from nonebot import on_regex, on_keyword
from utils.message_builder import record
from services.log import logger
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent
from nonebot.params import RegexGroup

__zx_plugin_name__ = "原神语音合成"
__plugin_usage__ = """
usage：
    你想让哪个原神角色说什么话？（不可以涩涩！）
    指令：
        [角色名]说[文本]
    示例：
        派蒙说你好呀旅行者。
        可莉说，大哥哥，要出去玩嘛？
    目前支持模型：
        '派蒙', '凯亚', '安柏', '丽莎', '琴', '香菱', '枫原万叶',
        '迪卢克', '温迪', '可莉', '早柚', '托马', '芭芭拉', 
        '优菈', '云堇', '钟离', '魈', '凝光', '雷电将军', '北斗', 
        '甘雨', '七七', '刻晴', '神里绫华', '戴因斯雷布', '雷泽', 
        '神里绫人', '罗莎莉亚', '阿贝多', '八重神子', '宵宫', 
        '荒泷一斗', '九条裟罗', '夜兰', '珊瑚宫心海', '五郎', 
        '散兵', '女士', '达达利亚', '莫娜', '班尼特', '申鹤', 
        '行秋', '烟绯', '久岐忍', '辛焱', '砂糖', '胡桃', '重云', 
        '菲谢尔', '诺艾尔', '迪奥娜', '鹿野院平藏'
""".strip()
__plugin_des__ = "原神人物语音合成"
__plugin_cmd__ = ["xx说"]
__plugin_version__ = 0.1
__plugin_type__ = ("原神相关",)
__plugin_author__ = "佚名" 
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["说"],
}

send_voice = on_keyword({"说"}, priority=5, block=True)
voice_reg = on_regex("(.*?)[说|说过](.*)$", priority=5, block=True)
path = "Paimon.wav"
list_ = ['派蒙', '凯亚', '安柏', '丽莎', '琴', '香菱', '枫原万叶', '迪卢克', '温迪', '可莉', '早柚', '托马', '芭芭拉', '优菈', '云堇', '钟离', '魈', '凝光', '雷电将军', '北斗', '甘雨', '七七', '刻晴', '神里绫华', '戴因斯雷布', '雷泽', '神里绫人', '罗莎莉亚', '阿贝多', '八重神子', '宵宫', '荒泷一斗', '九条裟罗', '夜兰', '珊瑚宫心海', '五郎', '散兵', '女士', '达达利亚', '莫娜', '班尼特', '申鹤', '行秋', '烟绯', '久岐忍', '辛焱', '砂糖', '胡桃', '重云', '菲谢尔', '诺艾尔', '迪奥娜', '鹿野院平藏']

@voice_reg.handle()
async def _(bot: Bot, event: MessageEvent, reg_group: Tuple[Any, ...] = RegexGroup()):
    speaker, text_ = reg_group
    await send_voice_handle(bot, event, speaker, text_)

async def send_voice_handle(bot: Bot, event: MessageEvent, speaker: str, text_: str):
    if speaker in list_:
        speaker = speaker
    else:
        await voice_reg.finish()
    text_ = text_
    if text_.startswith(",") or text_.startswith("，"):
        text_ = text_[1:]
    if len(text_) > 100:
        await send_voice.finish('太长了，小真寻说不完...')
    if len(str((event.get_message()))) > 1:
        global path
        url = "http://233366.proxy.nscc-gz.cn:8888/?speaker="
        url2 = "&format=wav&text="
        url = str(url + speaker + url2 + text_)
        path = path
        await AsyncHttpx.download_file(url, path)
        voice = "/home/zhenxun_bot/Paimon.wav"
        result = record(voice)
        await send_voice.send(result)
        logger.info(
            f"USER {event.user_id} GROUP "
            f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'} {
speaker} 说 {text_}"
        )

