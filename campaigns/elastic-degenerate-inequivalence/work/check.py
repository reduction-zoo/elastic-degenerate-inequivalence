"""Independent 3-SAT and split-graph star-coloring oracles."""

import argparse
import json
import subprocess
import sys
from itertools import permutations, product
from pathlib import Path

import z3


def legal_source(source):
    if not isinstance(source, dict):
        return False
    n = source.get("num_vars")
    clauses = source.get("clauses")
    return (type(n) is int and n >= 0 and isinstance(clauses, list)
            and all(isinstance(clause, list) and len(clause) <= 3
                    and all(type(literal) is int and 1 <= abs(literal) <= n for literal in clause)
                    for clause in clauses))


def solve_source(source):
    if not legal_source(source):
        raise ValueError("Illegal source formula")
    variables = [z3.Bool(f"x{i}") for i in range(source["num_vars"])]
    solver = z3.Solver()
    for clause in source["clauses"]:
        solver.add(z3.Or(*(variables[abs(literal) - 1] if literal > 0
                           else z3.Not(variables[-literal - 1]) for literal in clause)))
    result = solver.check()
    if result == z3.unsat:
        return {"status": "NO-SOLUTION"}
    if result != z3.sat:
        raise RuntimeError(f"Inconclusive source solver: {result}")
    model = solver.model()
    return {"assignment": [z3.is_true(model.eval(variable, model_completion=True)) for variable in variables]}


def valid_source(source, output):
    if not legal_source(source) or not isinstance(output, dict):
        return False
    if output == {"status": "NO-SOLUTION"}:
        return solve_source(source) == output
    assignment = output.get("assignment")
    if set(output) != {"assignment"} or not isinstance(assignment, list) or len(assignment) != source["num_vars"] or any(type(value) is not bool for value in assignment):
        return False
    return all(any(assignment[abs(literal) - 1] == (literal > 0) for literal in clause)
               for clause in source["clauses"])


def legal_target(target):
    if not isinstance(target,dict) or set(target) != {"left","right"}:
        return False
    return all(isinstance(target[side],list)
               and all(isinstance(options,list) and all(isinstance(word,str) for word in options)
                       and len(options) == len(set(options)) for options in target[side])
               for side in ("left","right"))


def language(slots):
    words = {""}
    for options in slots:
        words = {prefix+suffix for prefix in words for suffix in options}
    return words


def direct_member(slots,word):
    positions = {0}
    for options in slots:
        positions = {position+len(option) for position in positions for option in options
                     if word.startswith(option,position)}
    return len(word) in positions


def target_solutions(target,limit=3):
    if not legal_target(target):
        raise ValueError("Illegal elastic-degenerate string pair")
    differences = sorted(language(target["left"]) ^ language(target["right"]))
    outputs = [{"word":word} for word in differences[:limit]]
    for output in outputs:
        word = output["word"]
        assert direct_member(target["left"],word) != direct_member(target["right"],word)
    return outputs or [{"status":"NO-SOLUTION"}]


def solve_target(target):
    return target_solutions(target,1)[0]


def valid_target(target,output):
    if not legal_target(target) or not isinstance(output,dict):
        return False
    if output == {"status":"NO-SOLUTION"}:
        return solve_target(target) == output
    return (set(output) == {"word"} and isinstance(output["word"],str)
            and direct_member(target["left"],output["word"])
            != direct_member(target["right"],output["word"]))


def exhaustive_language(slots):
    return {"".join(parts) for parts in product(*slots)}


def self_test():
    from generate_cases import EDGE_CASES,random_source
    from test_oracle import test_hand_cases
    root = Path(__file__).resolve().parents[3]
    path = Path(__file__).with_name("cases.json")
    subprocess.run([sys.executable,str(root/"research/validate_preparation.py"),str(path)],check=True,cwd=root)
    cases = json.loads(path.read_text())
    for n,clauses,answer in EDGE_CASES:
        assert ("assignment" in solve_source({"num_vars":n,"clauses":clauses})) == answer
    for case in cases:
        source = case["source"]
        if case["kind"] == "random":
            assert random_source(case["seed"]) == source
        current = solve_source(source)
        exists = any(all(any(bits[abs(lit)-1] == (lit > 0) for lit in clause)
                             for clause in source["clauses"])
                     for bits in product((False,True),repeat=source["num_vars"]))
        assert ("assignment" in current) == exists == ("assignment" in case["expected"])
        assert valid_source(source,current) and valid_source(source,case["expected"])
    test_hand_cases()
    import random
    checked = 0
    for seed in range(120):
        rng = random.Random(seed)
        def random_slots():
            return [list(dict.fromkeys("".join(rng.choice("ab") for _ in range(rng.randrange(3)))
                                           for _ in range(rng.randrange(4))))
                    for _ in range(rng.randrange(4))]
        target = {"left":random_slots(),"right":random_slots()}
        left,right = exhaustive_language(target["left"]),exhaustive_language(target["right"])
        assert language(target["left"]) == left and language(target["right"]) == right
        assert ("word" in solve_target(target)) == (left != right)
        for word in left | right | {"", "abba"}:
            assert direct_member(target["left"],word) == (word in left)
            assert direct_member(target["right"],word) == (word in right)
        checked += 1
    print(f"Self-test passed: {len(cases)} source formulas and {checked} independent language comparisons")


def candidate_check(path):
    self_test()
    cases = json.loads(Path(__file__).with_name("cases.json").read_text())
    recovered = 0
    for case in cases:
        source = case["source"]
        forward = subprocess.run([sys.executable,str(path)],input=json.dumps(source),text=True,capture_output=True,check=True)
        target = json.loads(forward.stdout)
        if not legal_target(target):
            raise AssertionError(f"Illegal target: {target}")
        for output in target_solutions(target):
            assert valid_target(target,output)
            payload = {"source":source,"target_solution":output}
            extraction = subprocess.run([sys.executable,str(path),"--extract"],input=json.dumps(payload),text=True,capture_output=True,check=True)
            recovered_output = json.loads(extraction.stdout)
            if not valid_source(source,recovered_output):
                raise AssertionError(f"Invalid recovery from {output}: {recovered_output}")
            recovered += 1
    print(f"Candidate check passed: {len(cases)} source cases, {recovered} target outputs")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test",action="store_true")
    group.add_argument("--candidate",type=Path)
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        candidate_check(args.candidate)
