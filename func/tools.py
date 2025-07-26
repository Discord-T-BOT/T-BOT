from typing import Union
from func.data import BOT_ADMIN

# 管理者チェックの関数
def is_bot_admin(user_id:int) -> bool:
    return user_id in BOT_ADMIN

def color_code(code:str) -> int:
    if "#" in code:
        a = code.replace("#", "")
    else:
        a = code

    return int(f"0x{a}", 16)