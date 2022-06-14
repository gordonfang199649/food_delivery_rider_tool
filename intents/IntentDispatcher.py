import importlib
from intents.dictionaries.IntentDictionary import patterns

"""
    intent - 使用者意圖判斷
    :author Gordon Fang
    :date 2022-06-11
"""

"""
    分派機器人回應的動作
    :param intent: 原始訊息
    :param cache: 注入進來的快取器
    :return Line 訊息封裝物件
"""

def dispatch(self, intent: str):
    for pattern, action in patterns.items():
        matched = pattern.match(intent)

        # 若無命中任一意圖，機器人則不回應訊息
        if matched:
            module = importlib.import_module(f'{action[0]}.{action[1]}')
            class_ = getattr(module, action[1])()
            return getattr(class_, action[2])(intent=intent, pattern=pattern)

    return None
