# Prepared contract

Source: `{"num_vars":n,"clauses":[[signed_literal,...],...]}` with at most three literals per clause. Output a satisfying Boolean `{"assignment":[...]}` or `{"status":"NO-SOLUTION"}`.

Target: `{"left":[[word,...],...],"right":[[word,...],...]}`. Each outer list is a sequence of finite sets of explicit strings; duplicate words within a set are invalid. Its language contains every concatenation choosing one word from each set. An empty sequence denotes `{" "}` with the space omitted, namely the singleton empty word; an empty option set denotes the empty language. A positive output `{"word":string}` belongs to exactly one language. `NO-SOLUTION` means the languages are equal.

`algorithm.py` reads source JSON from stdin and emits legal target JSON. `algorithm.py --extract` reads `{"source":source,"target_solution":output}` and emits a valid source output. Both commands are deterministic, polynomial time, independent subprocesses. Errors exit nonzero; diagnostics go to stderr. Recovery must handle every valid target output.
