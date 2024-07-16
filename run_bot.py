import time

from highrise.__main__ import *
from highrise.__main__ import BotDefinition

bot_file_name = "main"
bot_class_name = "MyBot"
room_id = "6618fea4094e71259d05f9a7"
bot_token = "e985ff3079840167380e579337ee3501fa49323d8df051038fca67b51dabaddd"

my_bot = BotDefinition(getattr(import_module(bot_file_name), bot_class_name)(), room_id, bot_token)

while True:
    try:
        definitions = [my_bot]
        arun(main(definitions))
    except Exception as e:
        print(f"An exception occourred: {e}")
        time.sleep(5)