import Challenge
open ElasticDegenerateInequivalence
example : language [] = [[]] := by native_decide
example : language [[]] = [] := by native_decide
example : targetWitness ([], [[]]) [] = true := by native_decide
example : targetWitness ([[[0],[1]]], [[[1],[0]]]) [0] = false := by native_decide
