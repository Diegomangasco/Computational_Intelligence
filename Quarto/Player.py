import main
import random
class RandomPlayer(main.Player):

    def __init__(self, quarto: main.main) -> None:
        super.__init__(quarto)
    
    def choose_piece(self) -> int:
        return random.randint(0, 15)

    def place_piece(self) -> tuple[int, int]:
        return random.randint(0, 3), random.randint(0, 3)