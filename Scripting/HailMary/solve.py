#!/usr/bin/env python3
import json
import numpy as np
from pwn import remote
from datetime import datetime, timezone

HOST = "localhost"
PORT = 25201

POP_SIZE = 100
GENE_LEN = 10
MUT_RATE = 0.1
MUT_STRENGTH = 0.1

with open('flag.txt', 'r') as file:
    expected_flag = file.read()

def random_population():
    return np.random.rand(POP_SIZE, GENE_LEN).tolist()

def crossover_and_mutate(parents):
    new_pop = []
    for _ in range(POP_SIZE):
        p1, p2 = parents[np.random.randint(len(parents))], parents[np.random.randint(len(parents))]
        child = [(a + b) / 2 for a, b in zip(p1, p2)]
        # mutation
        for i in range(GENE_LEN):
            if np.random.rand() < MUT_RATE:
                child[i] = min(1.0, max(0.0, child[i] + np.random.normal(0, MUT_STRENGTH)))
        new_pop.append(child)
    return new_pop

def main():
    r = remote(HOST, PORT)
    welcome = r.recvuntil(b"science!\n\n")
    print(welcome.decode().strip())

    population = random_population()

    for gen in range(1, 999):
        if gen % 100 == 0:
            population = random_population()
            
        payload = json.dumps({"samples": population})
        r.sendline(payload.encode())
        try:
            resp = r.recvline().decode().strip()
            resp = json.loads(resp)
        except:
            if expected_flag in resp:
                print(f"✅ Challenge up as of {datetime.now(timezone.utc).isoformat()}. Flag confirmed to be {expected_flag}")
                print(resp)
                exit(0)
            else:
                print(f"❌ Challenge DOWN as of {datetime.now(timezone.utc).isoformat()}. Response from the server: {resp}")
                exit(1)

        scores = resp["scores"]
        avg = resp["average"]
        print(f"Gen {gen}: avg={avg:.4f}")

        # pick top 20% as parents
        scored = list(zip(population, scores))
        scored.sort(key=lambda x: x[1], reverse=True)
        parents = [x[0] for x in scored[:POP_SIZE // 5]]

        population = crossover_and_mutate(parents)

    r.close()
    print("Gene test failed.")
    exit(0)

if __name__ == "__main__":
    main()
