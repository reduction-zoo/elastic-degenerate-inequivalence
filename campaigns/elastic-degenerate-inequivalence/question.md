# 3-SAT → Elastic-degenerate string inequivalence

Category: Complexity open

## Source

A source instance is an explicitly encoded Boolean formula with at most three literals per clause. Its outputs are satisfying Boolean assignments, or NO-SOLUTION when the formula is unsatisfiable.

## Target

Each target string is a sequence of finite sets of explicit words; concatenation defines its finite language. Find a word in the symmetric difference of the two languages, or report that the languages are equal. Nested language expressions are not allowed.

## Required result

Construct deterministic polynomial-time maps F and G: F sends every legal source instance to a legal target instance, and G(x,y) is a valid source output for every valid output y of F(x). Preserve the stated threshold, domain and promises. The requested complexity conclusion is NP-hardness for the stated target problem.

## Acceptance

Give explicit construction and recovery algorithms, a general proof for every legal input and every valid target output, and polynomial runtime and encoding-size bounds. Specify finite output encodings and handle NO-SOLUTION outputs when applicable. Tests compare recovered source outputs with independent source solutions.

## Why it matters

The question concerns the cost of comparing compact representations of uncertain strings.

## Difficulty

Flattening unions can cause exponential growth, so a valid reduction must retain a polynomial explicit representation.

## Literature context

General regular-expression inequivalence does not immediately settle this finite, non-nested representation of string languages.

Literature checked 2026-09-16. This summarizes the archived literature search on the date above. Unpublished, unindexed and overlooked work remains outside coverage; no new novelty assessment was performed.

## References

- [Hardness Results on Characteristics for Elastic-Degenerate Strings](https://drops.dagstuhl.de/storage/00lipics/lipics-vol369-cpm2026/LIPIcs.CPM.2026.14/LIPIcs.CPM.2026.14.pdf): Koppl and Olbrich, Hardness Results on Characteristics for Elastic-Degenerate Strings, CPM 2026, Appendix C, printed page 14:25, leaves ordinary ED inequivalence open. It proves hardness for an extension permitting one level of nesting: a union of clause-falsification languages is compared with all binary assignments. Hardness for general star-free regular expressions does not establish hardness for flat ED strings. GD strings, whose alternatives in each segment have equal length, also differ from arbitrary ED strings.
- [2024 preprint](https://arxiv.org/abs/2411.10653): On 2026-09-16 searched "elastic-degenerate" "inequivalence", "elastic-degenerate" "equivalence" complexity 2026, and "Hardness Results on Characteristics" arxiv. Identified the 2024 preprint and inspected the later proceedings definitions and Appendix C. No later resolution was identified. Other finite-language factorization aliases remain outside this bounded coverage. Present openness is supported within coverage, not guaranteed.

Fixed from board record `website/questions/elastic-degenerate-inequivalence.json` in board checkout at 6c7d3bd9c0a8f595279969a9c0a4d1853a3f5c17; the record was copied from the current working tree.
