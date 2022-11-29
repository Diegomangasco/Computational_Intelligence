def cook_status(nim: Nim) -> dict:
    cooked = dict()
    cooked['possible_moves'] = [(r, o) for r, c in enumerate(nim._rows) for o in range(1, c + 1) if nim._k is None or o <= nim._k]
    cooked['active_rows_number'] = sum(r > 0 for r in nim._rows)
    cooked['shortest_row'] = min((x for x in enumerate(nim._rows) if x[1] > 0), key= lambda y: y[1])[0]
    cooked['longest_row'] = max((x for x in enumerate(nim._rows) if x[1] > 0), key= lambda y: y[1])[0]
    cooked['nim_status'] = verify_state(nim)

    brute_force = list()
    for m in cooked['possible_moves']:
        nim.nimming_remove()
    return cooked

def evaluate():
    pass

def make_strategy(genome: dict) -> Callable:
    def evolvable(nim: Nim) -> tuple:
        data = cook_status(nim)
        genome

        if random.random() < genome['p']:
            ply = (data['shortest_row'], random.randint(1, nim._rows[data['shortest_row']]))
        else:
            ply = (data['longest_row'], random.randint(1, nim._rows[data['longest_row']]))
        
        return ply
    return evolvable