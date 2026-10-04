import csv
import os
import json
import re
from collections import defaultdict


def score_contains(response, expected):
    return 1 if expected.lower() in response.lower() else 0


def find_numbers(text):
    return re.findall(r"-?\d+(?:\.\d+)?", text)


def score_math(response, expected):
    text = response.replace(",", "")
    bold_parts = re.findall(r"\*\*(.+?)\*\*", text)
    for part in reversed(bold_parts):
        nums = find_numbers(part)
        if nums:
            return 1 if float(nums[-1]) == float(expected) else 0
    nums = find_numbers(text)
    if not nums:
        return 0
    return 1 if float(nums[-1]) == float(expected) else 0


def score_yes_no(response, expected):
    words = response.replace("*", "").strip().lower().split()
    if not words:
        return 0
    first = words[0].strip(".,:;!")
    return 1 if first == expected.lower() else 0


METHODS = {
    "factual": score_contains,
    "math": score_math,
    "logic": score_yes_no,
    "reading": score_yes_no,
}


def load_manual():
    manual = {}
    path = "data/manual_scores.csv"
    if os.path.exists(path):
        with open(path) as f:
            for row in csv.DictReader(f):
                manual[(row["id"], row["model"], row["run"])] = int(row["manual_score"])
    return manual


def main():
    with open("data/questions.json") as f:
        questions = {q["id"]: q for q in json.load(f)}

    rows = []
    manual = load_manual()
    with open("data/responses.jsonl") as f:
        for line in f:
            r = json.loads(line)
            q = questions[r["id"]]
            category = q["category"]
            response = r["response"] or ""

            if category in METHODS:
                auto_score = METHODS[category](response, q["answer"])
                status = "auto"
            else:
                key = (r["id"], r["model"], str(r["run"]))
                if key in manual:
                    auto_score = manual[key]
                    status = "manual-done"
                else:
                    auto_score = ""
                    status = "manual"

            rows.append({
                "id": r["id"],
                "model": r["model"],
                "run": r["run"],
                "category": category,
                "auto_score": auto_score,
                "status": status,
            })

    with open("data/scores.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    totals = defaultdict(lambda: [0, 0])
    for row in rows:
        if row["status"] in ("auto", "manual-done"):
            key = (row["model"], row["category"])
            totals[key][0] += row["auto_score"]
            totals[key][1] += 1

    print("Wrote", len(rows), "rows to data/scores.csv")
    for (model, cat), (right, n) in sorted(totals.items()):
        print(model, cat, str(right) + "/" + str(n))


main()