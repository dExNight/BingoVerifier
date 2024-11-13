import asyncio
import json
import redis
from utils.bingo import BingoContract
from utils.wallet import BignoWallet
from config import IS_MAINNET

admin_address: str = "EQAAeHjRVfqPfRIjkPlxcv-OAffJUfAxWSu6RFli4FUeUMIo"

redis_client = redis.StrictRedis.from_url("redis://localhost:6379")


async def produce_task(task: dict):
    redis_client.lpush("bingo", json.dumps(task))


async def main():
    game_id: int = int(input("Enter game id: "))

    bingo: BingoContract = BingoContract(game_id, admin_address)

    print(f"Game #{game_id} contract:",
          bingo.get_address().to_str(is_test_only=not IS_MAINNET))

    # process raffle
    wallet: BignoWallet = BignoWallet()

    msg_body, value = bingo.get_raffle_msg()
    hash = await wallet.send_transfer(bingo.get_address().to_str(), value, msg_body, bingo.calculate_state_init())

    task = {
        "address": bingo.get_address().to_str(is_test_only=not IS_MAINNET),
    }
    await produce_task(task)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
