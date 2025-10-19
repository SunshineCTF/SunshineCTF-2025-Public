#!/usr/bin/env python3
import sys
import json
import math
import numpy as np 

MAX_GENERATIONS = 100
THRESHOLD = 0.95
PERCENT = THRESHOLD * 100
FLAG = "sun{wh4t_4_gr34t_pr0j3ct}"

def evaluate(weights, gene):
    clipped_array_so_users_cannot_cheese=np.clip(gene, 0, 1)
    return float(1 / (1 + np.exp(-np.dot(weights, clipped_array_so_users_cannot_cheese))))

def gen_weights():
    verify=[]
    null_check=[0,0,0,0,0,0,0,0,0,0]
    one_check=[1,1,1,1,1,1,1,1,1,1]
    half_check=[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]
    weights = np.random.uniform(-1, 1, 10)
    for value in weights:
        if value < 0:
            verify.append(0)
        else:
            verify.append(1)
    # remove unsolvable weight
    if evaluate(weights, verify) <= THRESHOLD:
        #sys.stderr.write(f"Weights != success {np.array2string(weights)}")
        #sys.stderr.flush()
        return gen_weights()
    # remove weights that are trivially solvable
    elif evaluate(weights, null_check) >= THRESHOLD or evaluate(weights, one_check) >= THRESHOLD or evaluate(weights, half_check) >= THRESHOLD:
        #sys.stderr.write(f"Bad weight trivially solvable {np.array2string(weights)}")
        #sys.stderr.flush()
        return gen_weights()
    return weights

weights=gen_weights()

def main():
    print(f"""
Welcome to the NASA Evolutionary Biology Lab! We are running tests on genetically modified taumoeba to try to optimize their survivability rating in alien atmospheres. You have {MAX_GENERATIONS} generations to attempt to reach an average of {PERCENT}% that survive. Submit populations of 100 gene samples, each 10 floats (0-1) in JSON format.
          
Example: {{"samples":[[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]....]}}
          
Good luck! The survival of Earth depends on your science!
"""
    )
    sys.stdout.flush()

    for generation in range(1, MAX_GENERATIONS + 1):
        try:
            raw = sys.stdin.readline()
            if not raw:
                break

            data = json.loads(raw.strip())
            genes = data.get("samples")

            if not genes or len(genes) != 100:
                print("Expected 100 samples")
                sys.stdout.flush()
                continue

            scores = [evaluate(weights, g) for g in genes]
            avg = sum(scores) / len(scores)

            if avg > THRESHOLD:
                print(f"Success! Earth has been saved! Here is your flag: {FLAG}")
                sys.stdout.flush()
                break
            elif math.isnan(avg):
                print(f"NaNNaNNaNNaN Batman! Not part of the challenge. Somehow you entered NaN.")
                sys.stdout.flush()
            else:
                print(json.dumps({
                    "generation": generation,
                    "average": avg,
                    "scores": scores
                }))
                sys.stdout.flush()

        except Exception as e:
            print("Error!")
            sys.stderr.write(e)
            sys.stdout.flush()

    else:
        print("Evolution failed. Your taumoeba did not evolve fast enough and Earth is now doomed.")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
