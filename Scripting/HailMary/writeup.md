# Hail Mary - Solution

## Misc (Medium)

In order to maximize the survivability of the population, players can use a genetic algorithm. They give a random population of genes to the service and get back a response, then pick out the top samples with the best score. Next, they combine random samples to simulate reproduction and then add a small amount of noise. The end result is that, with each concurrent generation, the scores will move towards a maximum by incremental improvement and eventually reach the threshold to get the flag.

The script below performs this process and will eventually get the flag after a few attempts. Some may fail due to random chance that they may find a local maximum but not the global.

```python
#!/usr/bin/env python3
import json
import numpy as np
from pwn import remote

HOST = "localhost"
PORT = 25201

POP_SIZE = 100
GENE_LEN = 10
MUT_RATE = 0.1
MUT_STRENGTH = 0.1

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

    for gen in range(1, 101):
        payload = json.dumps({"samples": population})
        r.sendline(payload.encode())
        try:
            resp = r.recvline().decode().strip()
            resp = json.loads(resp)
        except:
            print(resp)

        scores = resp["scores"]
        avg = resp["average"]
        print(f"Gen {gen}: avg={avg:.4f}")

        # pick top 20% as parents
        scored = list(zip(population, scores))
        scored.sort(key=lambda x: x[1], reverse=True)
        parents = [x[0] for x in scored[:POP_SIZE // 5]]

        population = crossover_and_mutate(parents)

    r.close()

if __name__ == "__main__":
    main()
```