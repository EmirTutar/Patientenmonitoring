import asyncio
from nio import AsyncClient, MatrixRoom, RoomMessageText
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()


async def message_callback(room: MatrixRoom, event: RoomMessageText) -> None:
    print(
        f"Message received in room {room.display_name}\n"
        f"{room.user_name(event.sender)} | {event.body}"
    )


async def main() -> None:

    homeserver_url = os.environ.get("MATRIX_HOMESERVER_URL")
    user_id = os.environ.get("MATRIX_USER_ID")
    print(user_id)
    password = os.environ.get("MATRIX_PASSWORD")
    room_id = os.environ.get("MATRIX_ROOM_ID")



    client = AsyncClient(homeserver_url,user_id)
    client.add_event_callback(message_callback, RoomMessageText)
    print(await client.login(password))

    await client.room_send(
        room_id=room_id,
        message_type="m.room.message",
        content={"msgtype": "m.text", "body": "Hello world!"},
    )
    await client.sync_forever(timeout=30000)  # milliseconds


asyncio.run(main())