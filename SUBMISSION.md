# Submission checklist — EF234405 DAA Final Exam

This project is complete and runnable. Before you email it, do the **five edits**
below (placeholders are marked `<...>`), rebuild the two PDFs, and zip them.

## 1. Fill in the team details (placeholders)

Edit the same block at the top of **both** generators:

* `report/build_report.py` → `MEMBERS`, `CLASS_NAME`, `GITHUB_URL`, `CONTRIB`,
  and the Student IDs.
* `report/build_declaration.py` → `MEMBERS`, `CITY_DATE`, `CONTRIB`.

Replace:
- `<Member 2 Full Name>`, `<Member 3 Full Name>` and the `50252210xx` IDs,
- `<D / IUP / E / F / G>` with your class,
- `<your-username>` in the GitHub URL,
- adjust the **contribution percentages/roles** to match reality.

(If your team is 2 people, delete the third member row in both files.)

## 2. Rebuild the PDFs

```bash
pip install fpdf2
python report/build_report.py        # -> report/Report.pdf
python report/build_declaration.py   # -> report/Declaration.pdf
```

## 3. Sign the declaration

Open `report/Declaration.pdf`, add each member's signature (handwritten scan or
digital) above their printed name. An **unsigned** declaration scores 0.

## 4. Reproduce the benchmark (already committed, but verify on a clean checkout)

```bash
./run_benchmark.sh
```

This regenerates `bench/results/timings.csv` and the figures. The numbers may
shift by a few percent between machines — that's expected; the report reads the
CSV at build time, so rebuild the report (step 2) after re-running if you want
the tables to match your machine exactly.

## 5. Package and email

**ZIP** — exactly two files at the archive root:

```
EF234405_DAA_FIN_<StudentID1>_<Name1>_<StudentID2>_<Name2>.ZIP
  ├── Report.pdf
  └── Declaration.pdf
```

```bash
cd report && zip ../EF234405_DAA_FIN_<ID1>_<Name1>_<ID2>_<Name2>.zip Report.pdf Declaration.pdf
```

**Email**
- **To:** yifana@gmail.com
- **CC:** the TA list in the exam brief (§1).
- **Subject:** `EF234405_DAA_FIN_StudentID1_Name1_StudentID2_Name2`
- **Body:** include the **public** GitHub repository link (push this repo to a
  public GitHub repo first; have each member commit under their own account
  during the week so individual participation is visible).

**Deadline:** 18 June 2026, 23:59 WIB. Late penalty 0.15%/minute.

---

### What's in this submission (rubric map)

| Rubric | Where |
|--------|-------|
| Design (D1–D4) | `report/Report.pdf` §1 |
| Implementation (I1–I5) | `src/`, `demo.py`, `report/Report.pdf` §2 |
| Analysis & Evaluation (A1–A5) | `report/Report.pdf` §3, `bench/results/` |
| Conclusion + contributions (C1) | `report/Report.pdf` §4 |
| Bonus (3rd algorithm: A*) | `src/astar.py`, throughout the report |
