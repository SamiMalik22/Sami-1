import asyncio
import importlib.util
import os
import random

from highrise import *
from highrise import BaseBot, Position, User, __main__
from highrise.models import *
from highrise.models import (
    Item,
    Position,
    SessionMetadata,
    User,
    CurrencyItem,
)

from webserver import keep_alive

name_ad =["BOWE._.0", "king_of_gambling"]
MESSAGES = ["Welcome to this room. You will find your soulmate here. Dont forget to use emotes (type from 2 to onward for emote) tip 500g to become vip "]


class BotDefinition:

  def __init__(self, bot, room_id, api_token):
    self.bot = bot
    self.room_id = room_id
    self.api_token = api_token


class MyBot(BaseBot):

  def __init__(self, bot, room_id, api_token):
    self.bot = bot
    self.room_id = room_id
    self.api_token = api_token

  dancs = [
      "idle-loop-sitfloor", "emote-tired", "emote-pose7", "emoji-thumbsup",
      "emoji-angry", "dance-macarena", "emote-hello", "dance-weird",
      "emote-superpose", "idle-lookup", "idle-hero", "emote-wings",
      "emote-laughing", "emote-kiss", "emote-wave", "emote-hearteyes",
      "emote-theatrical", "emote-teleporting", "emote-slap", "emote-ropepull",
      "emote-think", "emote-hot", "dance-shoppingcart", "emote-greedy",
      "emote-frustrated", "emote-float", "emote-baseball", "emote-yes",
      "idle_singing", "idle-floorsleeping", "idle-loop-sitfloor",
      "idle-enthusiastic", "emote-confused", "emoji-celebrate", "emote-no",
      "emote-swordfight", "emote-shy", "dance-tiktok2", "emote-model",
      "emote-charging", "emote-snake", "dance-russian", "emote-sad",
      "emote-lust", "emoji-cursing", "emoji-flex", "emoji-gagging",
      "dance-tiktok8", "dance-blackpink", "dance-pennywise", "emote-bow",
      "emote-curtsy", "emote-snowball", "emote-snowangel", "emote-telekinesis",
      "idle-dance-tiktok4"
      "emote-maniac", "emote-energyball", "emote-frog", "emote-cute",
      "dance-tiktok9", "dance-tiktok10", "emote-pose7", "emote-pose8",
      "idle-dance-casual", "emote-pose1", "dance-sexy", "emote-pose3",
      "emote-pose5", "emote-cutey", "emote-Relaxing", "emote-model",
      "emote-fashionista", "emote-gravity", "emote-zombierun",
      "emoji-ceilebrate", "emoji-floss", "emote-Relaxing ", "emote-punkguitar",
      "dance-tiktok9", "dance-weird", "emote-punkguitar", "idle-uwu"
      "emote-swordfight", "emote-handstand", "emote-bow", "emote-cursty",
      "dance-breakdance", "emote-creepycute", "emote-headblowup", "idle-guitar"
  ]
  dans = [
      "dance-blackpink",
      "emote-punkguitar",
      "emote-telekinesis",
      "dance-tiktok2",
      "dance-tiktok8",
      "dance-weird",
      "dance-russian",
      "idle_singing",
      "idle-dance-casual",
  ]

  async def on_reaction(self, user: User, reaction: Reaction,
                        receiver: User) -> None:
    if reaction == "heart" and user.username in name_ad:
      r_username = receiver.username
      print(f"receiver: {r_username}")
      list = await self.highrise.get_room_users()
      username_targ = user.username
      for user, position in list.content:
        if user.username == username_targ:
          print(f"User: {user.username}")
          print(f"id: {user.id}")
          positions = f"{position.x}, {position.y}, {position.z}"
          await self.highrise.teleport(
              receiver.id,
              Position(x=position.x, y=position.y, z=position.z - 1))

  async def loop(self) -> None:
    while True:
      emote_id = random.choice(self.dans)
      await self.highrise.send_emote(emote_id)
      await asyncio.sleep(5)

  async def send_periodic_message(self):
    try:
      while True:
        message = random.choice(MESSAGES)
        await self.highrise.chat(message)
        await asyncio.sleep(120)  # 2 minutes
    except Exception as e:
      print(f"An exception occurred: {e}")

  async def on_user_move(self, user: User, pos: Position) -> None:
    print(f"{user.username} moved to {pos}")

  async def on_start(self, session_metadata: SessionMetadata) -> None:
    print("[Start]")
    self.highrise.tg.create_task(coro=self.loop())
    room_users = (await self.highrise.get_room_users()).content
    if any(u[0].id == session_metadata.user_id for u in room_users):
      await self.highrise.teleport(session_metadata.user_id,
                                  Position(x=18, y=0.0, z=7.0, facing='FrontRight'))
    else:
      print("User is not present in the room")
    try:

      send_task = asyncio.create_task(self.send_periodic_message())
      await asyncio.gather(send_task)
    except Exception as e:
      print(f"An exception occurred: {e}")

  async def on_user_join(self, user: User, position: str) -> None:
    try:
      room_users = (await self.highrise.get_room_users()).content
      user_present = any(u[0].id == user.id for u in room_users)
      if user_present:

        await self.highrise.chat(
            f"welcome to this room to use any emote type from 2 to onward    {user.username}")
        emote_id = random.choice(self.dancs)
        await self.highrise.send_emote(emote_id, user.id)
      else:
        print("User has left the room")
    except:
      print("Error sending whisper")

  async def command_handler(self, user: User, message: str):
    parts = message.split(" ")
    command = parts[0][1:]
    functions_folder = "functions"
    # Check if the function exists in the module
    for file_name in os.listdir(functions_folder):
      if file_name.endswith(".py"):
        module_name = file_name[:-3]  # Remove the '.py' extension
        module_path = os.path.join(functions_folder, file_name)

        # Load the module
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Check if the function exists in the module
        if hasattr(module, command) and callable(getattr(module, command)):
          function = getattr(module, command)
          await function(self, user, message)

    # If no matching function is found
    return

  async def on_tip(self, sender: User, receiver: User, tip: CurrencyItem | Item) -> None:
      if tip.amount > 299 and receiver.username in ["suraiko","pikocki","bestboy46","TheDesiBot"] and sender.username not in name_ad:
          await self.highrise.teleport(sender.id, Position(x=3.5, y=17.0, z=4.5, facing='FrontRight'))

  async def on_chat(self, user: User, message: str) -> None:
    if message.lower().startswith('/'):
      await self.command_handler(user, message)

    if message.startswith("0"):
      await self.highrise.send_emote("emote-float", user.id)
    if message.startswith("2"):
      await self.highrise.send_emote("dance-tiktok2", user.id)   
    if message.startswith("3"):
      await self.highrise.send_emote("emote-pose1", user.id)
    if message.startswith("4"):
      await self.highrise.send_emote("dance-shoppingcart", user.id)
    if message.startswith("5"):
      await self.highrise.send_emote("dance-russian", user.id)
    if message.startswith("6"):
      await self.highrise.send_emote("idle_singing", user.id)
    if message.startswith("7"):
      await self.highrise.send_emote("idle-enthusiastic", user.id)   
    if message.startswith("8"):
      await self.highrise.send_emote("idle-dance-casual", user.id)   
    if message.startswith("9"):
      await self.highrise.send_emote("idle-loop-sitfloor", user.id)
    if message.startswith("10"):
      await self.highrise.send_emote("emote-lust", user.id)
    if message.startswith("11"):
      await self.highrise.send_emote("emote-greedy", user.id)
    if message.startswith("12"):
      await self.highrise.send_emote("emote-bow", user.id)
    if message.startswith("13"):
      await self.highrise.send_emote("emote-curtsy", user.id)
    if message.startswith("14"):
      await self.highrise.send_emote("emote-snowball", user.id)
    if message.startswith("15"):
      await self.highrise.send_emote("emote-snowangel", user.id)
    if message.startswith("16"):
      await self.highrise.send_emote("emote-confused", user.id)
    if message.startswith("17"):
      await self.highrise.send_emote("emote-teleporting", user.id)
    if message.startswith("18"):
      await self.highrise.send_emote("emote-swordfight", user.id)
    if message.startswith("19"):
      await self.highrise.send_emote("emote-energyball", user.id)
    if message.startswith("20"):
      await self.highrise.send_emote("dance-tiktok8", user.id)
    if message.startswith("21"):
      await self.highrise.send_emote("dance-blackpink", user.id)
    if message.startswith("22"):
      await self.highrise.send_emote("emote-model", user.id)
    if message.startswith("23"):
      await self.highrise.send_emote("dance-pennywise", user.id)
    if message.startswith("24"):
      await self.highrise.send_emote("dance-tiktok10", user.id)
    if message.startswith("25"):
      await self.highrise.send_emote("emote-telekinesis", user.id)
    if message.startswith("26"):
      await self.highrise.send_emote("emote-hot", user.id)
    if message.startswith("27"):
      await self.highrise.send_emote("dance-weird", user.id)
    if message.startswith("28"):
      await self.highrise.send_emote("emote-pose7", user.id)
    if message.startswith("29"):
      await self.highrise.send_emote("emote-pose8", user.id)
    if message.startswith("30"):
      await self.highrise.send_emote("emote-pose3", user.id)
    if message.startswith("31"):
      await self.highrise.send_emote("emote-pose5", user.id)  
    if message.startswith("32"):
      await self.highrise.send_emote("emote-pose5", user.id)  
    if message.startswith("31"):
      await self.highrise.send_emote("emote-pose5", user.id)  
    if message.startswith("31"):
      await self.highrise.send_emote("emote-pose5", user.id)

    if message in ["vip","Vip","!vip","!Vip"] and user.username in name_ad:
        try:
          await self.highrise.teleport(f"{user.id}",Position(x=12.0, y=17.5, z=4.5, facing='FrontRight'))
        except Exception as e:
          print(f"Error: {e}")

    if message in ["Down","down","!Down","!down"]:
        try:
          await self.highrise.teleport(f"{user.id}",Position(x=18.0, y=0.0, z=7.0, facing='FrontRight'))
        except Exception as e:
          print(f"Error: {e}")

  
  async def run(self):

    definitions = [BotDefinition(self, self.room_id, self.api_token)]
    await __main__.main(definitions)

  # Attempt to reconnect after a delay


keep_alive()
if __name__ == "__main__":
  room_id = "665569b456e3ef3bfe0e1c1c"
  token = "495ae9bc523e304c9d79056dfe806382c827594f4b17118cb95a423dafb950d9"
  bot = Highrise()
  bot_instance = MyBot(bot, room_id, token)
  asyncio.run(bot_instance.run())
