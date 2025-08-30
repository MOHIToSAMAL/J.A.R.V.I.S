import json
from Model import FirstLayerDMM

# ---- Judge function ----
def judge_output(expected, got):
    """
    Simple semantic judge:
    Returns {"score":0|1,"reason": "..."}
    """
    # Exact match
    if got == expected:
        return {"score": 1, "reason": "Exact match"}

    # Partial / semantic check
    got_join = " ".join(got).lower()
    exp_join = " ".join(expected).lower()

    if exp_join in got_join or got_join in exp_join:
        return {"score": 1, "reason": "Semantically similar"}

    return {"score": 0, "reason": f"Mismatch (expected {expected}, got {got})"}


# ---- Main Eval ----
with open("Data/eval.json","r",encoding="utf-8") as f:
    tests=json.load(f)

report=[]
passed=0
for t in tests:
    out = FirstLayerDMM(t["prompt"])
    result = judge_output(t["expected"], out)
    passed += result["score"]
    report.append({
        "prompt": t["prompt"],
        "expected": t["expected"],
        "got": out,
        "pass": bool(result["score"]),
        "reason": result["reason"]
    })

with open("Data/eval_results.json","w",encoding="utf-8") as f:
    json.dump({"passed":passed,"total":len(tests),"cases":report},f,indent=2)

print(f"Passed {passed}/{len(tests)}")
