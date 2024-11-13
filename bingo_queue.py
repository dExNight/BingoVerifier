import asyncio
import json
import redis
from utils.tonapi import Tonapi, MethodExecutionResult
from utils.verifier import RaffleVerifier
from pytoniq_core import Cell, Address


redis_client = redis.StrictRedis.from_url("redis://localhost:6379")


async def consume_tasks():
    queue_result = redis_client.brpop("bingo", timeout=1)

    if not queue_result:
        await asyncio.sleep(1)
        return

    _, task_json = queue_result
    task = json.loads(task_json)
    print(f'Consumed: {task["address"]}')

    try:

        result: MethodExecutionResult = await Tonapi().execute_get_method(task["address"], "raffle_data")

        if not result.success:
            redis_client.lpush("bingo", task_json)
            return

        init: bool = int(result.stack[0].num, 16) == 1
        if not init:
            redis_client.lpush("bingo", task_json)
            return

        game_id: int = int(result.stack[1].num, 16)
        admin_address: Address = Cell.one_from_boc(result.stack[2].cell).begin_parse().load_address()
        seed: int = int(result.stack[3].num, 16)

        verifier: RaffleVerifier = RaffleVerifier()
        sequence = verifier.generate_sequence(seed)

        print(f"Game ID: {game_id}")
        print(f"Sequence: {sequence}")

        # TODO: process generated sequence

    except Exception as e:
        print(f"EXCEPTION RAISED: {e}")
        redis_client.lpush("bingo", task_json)


async def infinite_consume():
    while True:
        await consume_tasks()
        await asyncio.sleep(3)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(infinite_consume())
