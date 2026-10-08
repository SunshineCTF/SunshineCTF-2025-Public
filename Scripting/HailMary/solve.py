#!/usr/bin/env python3
# Genetic-algorithm solver for the NASA "Hail Mary" taumoeba challenge.
#
# The server scores a population of 100 gene vectors (10 floats in [0,1]) with
# sigmoid(dot(weights, gene)) and wants the population *average* above 0.95
# within 100 generations. We evolve the population toward the (unknown) optimal
# vertex using the per-sample scores the server returns: keep the best genes
# (elitism), breed the top performers, and mutate. The dot-product is monotonic
# so selection pressure quickly drives every gene to the correct 0/1 corner.
#
# Ported off numpy to the stdlib `random` module so it runs in the pwnmake
# check container with only pwntools installed.
import os
import sys
import json
import random
from pwn import remote
from datetime import datetime, timezone

HOST = os.environ.get("HOST", "localhost")
PORT = int(os.environ.get("PORT", 25201))

POP_SIZE = 100
GENE_LEN = 10
MUT_RATE = 0.2
MUT_STRENGTH = 0.25

with open('flag.txt', 'r') as file:
    expected_flag = file.read().strip()


def random_population():
    return [[random.random() for _ in range(GENE_LEN)] for _ in range(POP_SIZE)]


def crossover_and_mutate(parents, elite):
    # Elitism: carry the best individuals through unchanged.
    new_pop = [list(g) for g in elite]
    while len(new_pop) < POP_SIZE:
        p1 = parents[random.randrange(len(parents))]
        p2 = parents[random.randrange(len(parents))]
        child = [(a + b) / 2 for a, b in zip(p1, p2)]
        # mutation
        for i in range(GENE_LEN):
            if random.random() < MUT_RATE:
                child[i] = min(1.0, max(0.0, child[i] + random.gauss(0, MUT_STRENGTH)))
        new_pop.append(child)
    return new_pop


def main():
    r = remote(HOST, PORT)
    welcome = r.recvuntil(b"science!\n\n")
    print(welcome.decode(errors="replace").strip())

    population = random_population()

    while True:
        payload = json.dumps({"samples": population})
        r.sendline(payload.encode())

        line = r.recvline().decode(errors="replace").strip()
        try:
            resp = json.loads(line)
        except Exception:
            # Non-JSON line: either the success message (with the flag) or the
            # failure message once generations run out.
            print(line)
            if expected_flag in line:
                print(f"Challenge up as of {datetime.now(timezone.utc).isoformat()}. "
                      f"Flag confirmed to be {expected_flag}")
                return 0
            print("Challenge did not yield the flag.")
            return 1

        scores = resp["scores"]
        avg = resp["average"]
        print(f"Gen {resp.get('generation', '?')}: avg={avg:.4f}")

        # Rank by score; keep top 20% as parents and the top 5 as elites.
        scored = sorted(zip(population, scores), key=lambda x: x[1], reverse=True)
        parents = [g for g, _ in scored[:POP_SIZE // 5]]
        elite = [g for g, _ in scored[:5]]
        population = crossover_and_mutate(parents, elite)


if __name__ == "__main__":
    sys.exit(main())
