# CareLoop Clinics — No-Show Guard

**Repository link:** <paste your public GitHub URL here>

## Summary (one finding per Part — replace every [ ] with YOUR output)
1. **Data:** 1,020 raw rows → [990] clean rows after removing [20] duplicates and [10] rows with unreadable date/status; [218] no-shows = [22.0]%.
2. **SQL:** highest rate among clinics with ≥95 bookings is [Hadapsar Care Centre, 27.3%]; no-shows rise from [16.2%] (lead 1–7 days) to [60.5%] (31+ days).
3. **Model:** [logistic regression] won on cross-validated training ROC-AUC ([0.77]); at threshold [0.35] it flags [~49] of 198 test bookings with recall [~0.57], precision [~0.57], test AUC [~0.79].
4. **GenAI:** [n] of 9 non-blank notes matched the expected reason; both "forgot / no reminder" notes belong to bookings with reminder_sent = No.

## Recommendation
[One paragraph answering "which appointments, why, what first", using ≥4 of your own numbers. Suggested shape: the riskiest bookings are those made far ahead (lead_days > 14: X% of bookings; 31+ days: 60.5% no-show), without a reminder (reminder_sent has the most negative coefficient; odds ratio ≈ X for No→Yes, an association not proof), and at the high-rate Pune/Jaipur clinics. First action: send reminders for every booking and phone the evening-before flagged list (about X calls per test-size sample), starting with long-lead bookings. The notes (only 10) hint at reminders, transport, cost and work as reasons.]

## Model chosen and why
[Model name], chosen **only from 5-fold cross-validated ROC-AUC on the training set** ([score]), compared with the depth-3 tree ([ ]), default forest ([ ]) and tuned forest ([ ]). Threshold **[0.35]** chosen from out-of-fold training probabilities (F1 [ ] vs [ ] at 0.5, higher recall). Test set used once: AUC [ ], precision [ ], recall [ ], flagged [ ]. Scores are in `test_risk_scores.csv`.

## Limitations (choose three, own words)
1. The 10 analysed notes illustrate the method and cannot show clinic-wide reasons.
2. Cleaning medians/fences were computed on all 990 rows before the split, so test rows slightly influenced the cleaning.
3. The same patient can be in both train and test, and the split is random rather than past-to-future.
(Alternatives: single split; threshold really depends on call capacity; small clinic samples; observational data.)

## Files
`01_ingest_clean.ipynb`, `rejected_rows.json`, `appointments_clean.csv`, `clinics_enriched.csv`, `load_data.sql`, `02_queries.sql`, `03_model.ipynb`, `test_risk_scores.csv`, `04_genai.ipynb` (key removed), `notes_analysed.csv`, `data/` (three originals).
