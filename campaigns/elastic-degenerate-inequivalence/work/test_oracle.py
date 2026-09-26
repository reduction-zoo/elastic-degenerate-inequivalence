from check import legal_target,solve_target,valid_target


def test_hand_cases():
    equal = {"left":[["a","b"],["c"]],"right":[["ac","bc"]]}
    assert solve_target(equal) == {"status":"NO-SOLUTION"}
    distinct = {"left":[["a","b"]],"right":[["a"]]}
    assert valid_target(distinct,{"word":"b"})
    assert not valid_target(distinct,{"word":"a"})
    assert valid_target({"left":[],"right":[[""]]},{"status":"NO-SOLUTION"})
    assert valid_target({"left":[[]],"right":[]},{"word":""})
    assert not legal_target({"left":[["a","a"]],"right":[]})


if __name__ == "__main__":
    test_hand_cases()
