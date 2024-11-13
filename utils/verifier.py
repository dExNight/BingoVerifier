from typing import List


class RaffleVerifier:
    def __init__(self,
                 TOTAL_NUMBERS: int = 90,
                 MULTIPLIER: int = 48271,
                 MODULUS: int = 2147483647):
        self.TOTAL_NUMBERS = TOTAL_NUMBERS
        self.MULTIPLIER = MULTIPLIER
        self.MODULUS = MODULUS

    def generate_sequence(self, game_seed: int) -> List[int]:
        if game_seed <= 0:
            raise ValueError('Invalid seed')

        numbers = list(range(1, self.TOTAL_NUMBERS + 1))
        seed = game_seed

        def next_random() -> int:
            nonlocal seed
            seed = (seed * self.MULTIPLIER) % self.MODULUS
            return seed

        for i in range(len(numbers) - 1, 0, -1):
            j = next_random() % (i + 1)
            numbers[i], numbers[j] = numbers[j], numbers[i]

        return numbers

    def verify_sequence(self, game_seed: int, sequence: List[int]) -> bool:
        expected_sequence = self.generate_sequence(game_seed)
        return sequence == expected_sequence
