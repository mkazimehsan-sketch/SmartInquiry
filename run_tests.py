"""Run the classifier against a CSV of test inquiries and report mismatches.

Usage:  python run_tests.py [csv_path] [output_name]
Defaults: data/sample_inquiries.csv  ->  docs/test_results_<output_name>.md
Each CSV needs columns: id, message, expected_category, needs_human_review
(order_id is optional).
"""
import csv
import sys
from pathlib import Path

from classifier import classify

ROOT = Path(__file__).parent


def run(csv_path: Path, out_name: str) -> int:
    rows = list(csv.DictReader(csv_path.open(encoding="utf-8")))
    lines, mismatches = [], []
    cat_ok = rev_ok = 0

    for r in rows:
        res = classify(r["message"], r.get("order_id", ""))
        exp_cat = r["expected_category"].strip()
        exp_rev = r["needs_human_review"].strip().lower() == "yes"
        c_ok, v_ok = res.category == exp_cat, res.needs_review == exp_rev
        cat_ok += c_ok
        rev_ok += v_ok
        status = "PASS" if (c_ok and v_ok) else "MISMATCH"
        lines.append((r["id"], r["message"], exp_cat, res.category, exp_rev, res.needs_review, status, res.reason))
        if status == "MISMATCH":
            mismatches.append(lines[-1])

    n = len(rows)
    md = [f"# Classifier test results - {csv_path.name}", "",
          f"- Inquiries tested: **{n}**",
          f"- Category correct: **{cat_ok}/{n}**",
          f"- Review flag correct: **{rev_ok}/{n}**",
          f"- Fully passing rows: **{n - len(mismatches)}/{n}**", "",
          "| ID | Message | Expected | Got | Review expected | Review got | Result |",
          "|----|---------|----------|-----|-----------------|------------|--------|"]
    for i, m, ec, gc, er, gr, st, _ in lines:
        short = (m[:60] + "...") if len(m) > 60 else m
        md.append(f"| {i} | {short.replace('|', '/')} | {ec} | {gc} | {'yes' if er else 'no'} | {'yes' if gr else 'no'} | {st} |")
    md += ["", "## Mismatches", ""]
    if mismatches:
        for i, m, ec, gc, er, gr, st, why in mismatches:
            md.append(f"- **#{i}** \"{m}\" - expected `{ec}` (review={er}), got `{gc}` (review={gr}). Reason given: {why}")
    else:
        md.append("None.")

    out = ROOT / "docs" / f"test_results_{out_name}.md"
    out.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"{csv_path.name}: {n - len(mismatches)}/{n} rows pass "
          f"(category {cat_ok}/{n}, review flag {rev_ok}/{n}) -> {out.relative_to(ROOT)}")
    for i, m, ec, gc, er, gr, st, why in mismatches:
        print(f"  MISMATCH #{i}: expected {ec}/{er}, got {gc}/{gr} | {m}")
    return len(mismatches)


if __name__ == "__main__":
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "data" / "sample_inquiries.csv"
    name = sys.argv[2] if len(sys.argv) > 2 else "sample"
    run(path, name)
