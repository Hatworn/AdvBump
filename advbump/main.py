import asyncio
import json

from bumper import Bumper

CONFIG_PATH = "config.json"


def get_config(path: str) -> dict:
    with open(path) as file:
        return json.load(file)


def create_bumper_tasks(accounts: list, action_duration: float, bump_cooldown: float, max_random_delay: float) -> list:
    tasks = []
    execution_delay = 0
    delay = action_duration / len(accounts)

    for account in accounts:
        token = account["token"]
        channel_id = account["channel_id"]

        bumper = Bumper(token, channel_id, execution_delay, bump_cooldown, max_random_delay)
        tasks.append(bumper.run())
        execution_delay += delay

    return tasks


async def main() -> None:
    config = get_config(CONFIG_PATH)

    accounts = config["accounts"]
    action_duration = config["action_duration"]
    bump_cooldown = config["bump_cooldown"]
    max_random_delay = config["max_random_delay"]

    tasks = create_bumper_tasks(accounts, action_duration, bump_cooldown, max_random_delay)
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
