
"""Generate old groups which are older than year 2023

requirements:

- api id
- api hash
- Pyrogram
- TgCrypto

Get your Telegram API Key from:
https://my.telegram.org/apps
"""

import asyncio
from pyrogram import Client
from pyrogram.enums import ChatType

async def main():
  api_id = int(input("API ID: "))
  api_hash = input("API HASH: ")
  client = Client(":memory:", api_id=api_id, api_hash=api_hash, in_memory=True)
  await client.start()
  await get_owner_dialogs(client)

async def get_owner_dialogs(client):
  async for d in client.get_dialogs():
    c = d.chat
    if c.is_creator and c.type in {ChatType.GROUP, ChatType.SUPERGROUP}:
      first = await client.get_messages(c.id, 1)
      if first.empty:
        oldest = await anext(
          client.get_chat_history(c.id, limit=1, offset_id=1, offset=-1), None
        )
        if oldest and not oldest.empty:
          first = oldest
        else:
          continue
      if not first.date.year < 2023:
        continue
      if c.username:
        link = f"https://t.me/{c.username}"
      else:
        link = (await client.get_chat(c.id)).invite_link
      await client.send_message(
        "me",
        f"{c.title} | {first.date.year} | {c.type.value.lower()}\n\n{link}",
        disable_web_page_preview=False,
      )
      
      
      

if __name__ == "__main__":
  loop = asyncio.get_event_loop()
  loop.run_until_complete(main())

print ("WORK IS OVER")
