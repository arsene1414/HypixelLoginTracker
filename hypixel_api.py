import aiohttp
import asyncio

class HypixelAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def get_player_data(self, player_name: str, session: aiohttp.ClientSession):
        headers = {"API-Key": self.api_key}
        params = {"name": player_name}
        backoff = 5

        while True:
            try:
                async with session.get("https://api.hypixel.net/v2/player", headers=headers, params=params) as resp:
                    if resp.status == 429:
                        await asyncio.sleep(backoff)
                        backoff = min(backoff * 2, 120)
                        continue

                    if resp.status != 200:
                        return None

                    data = await resp.json()
                    if not data.get("success", False):
                        return None

                    return data
            except aiohttp.ClientError:
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, 120)
            except Exception:
                return None

    @staticmethod
    def is_player_online(data):
        if not data or not data.get("player"):
            return False
        player = data["player"]
        last_login = player.get("lastLogin")
        last_logout = player.get("lastLogout")
        return last_login and last_logout and last_login > last_logout
