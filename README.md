# CareLoop Clinics — No-Show Guard

**Repository link:** https://github.com/Kiaat/CapstoneProject

## Summary
1. **Data (Part 1):** 1,020 raw rows became 990 clean rows (20 duplicates and 10 rows with an unreadable date or blank status removed); 218 of 990 bookings are no-shows (22.0%).
2. **SQL (Part 2):** among clinics with at least 95 bookings, Hadapsar Care Centre has the highest no-show rate (27.3%); no-shows climb from 16.2% for bookings made 1–7 days ahead to 60.5% for bookings made 31+ days ahead.
3. **Model (Part 3):** logistic regression was chosen on cross-validated training ROC-AUC (0.774); at a 0.35 threshold it flags 49 of 198 test bookings with precision 0.571, recall 0.571 and test ROC-AUC 0.789.
4. **GenAI (Part 4):** [FILL AFTER YOUR GEMINI RUN: "n of 9 non-blank notes matched the expected reason; both 'forgot / no reminder' notes (N001, N007) belong to bookings with reminder_sent = No."]

## Recommendation
[Rewrite in your own words. Suggested content, all numbers from your outputs:] The bookings most likely to be missed are those made far ahead and those with no reminder. Only 16.2% of bookings made 1–7 days ahead are missed, but 30.0% of bookings made 15–30 days ahead and 60.5% of those made 31+ days ahead are. In the logistic regression, a reminder is associated with about 69% lower odds of a no-show (odds ratio 0.31, holding the other features constant; an association, not proof of cause), and 5 of the 10 analysed notes belong to bookings with no reminder. Hadapsar Care Centre (27.3%) and Malviya Nagar Clinic (26.8%) have the highest rates among the larger clinics. What to do first: make sure every booking gets a reminder, send an extra reminder for bookings made more than 14 days ahead (29.9% of bookings), and let the front desk phone the roughly 49 bookings per 198 that the model flags the evening before, starting with the long-lead ones. [Add one sentence on why patients miss, from your Part 4 crosstab.]

## Model chosen and why
Logistic regression (with a scaler inside a pipeline), chosen **only from 5-fold cross-validated ROC-AUC on the training set**: logistic regression 0.774, tuned random forest 0.767 (best parameters max_depth=3, n_estimators=200), default random forest 0.747, depth-3 tree 0.678. The threshold **0.35** was chosen from out-of-fold training probabilities: F1 0.489 and recall 0.467 at 0.35, against F1 0.347 and recall 0.249 at 0.5; a missed warning costs an empty slot while an extra call costs a minute, so recall matters. The test set was used once: precision 0.571, recall 0.571, 49 flagged, ROC-AUC 0.789. The scores are in `test_risk_scores.csv`. In practice a clinic would pick the threshold by how many follow-up calls the front desk can make in an evening, against the cost of an empty slot.

## Limitations
1. The 10 analysed notes are an illustration and cannot show the real reasons clinic-wide.
2. The cleaning statistics (medians, quartiles, fences) came from all 990 rows before the split, so the test rows slightly influenced the cleaning.
3. The same patient can appear in both train and test, and the split is random rather than past-to-future; the data are also observational, so associations such as the reminder effect are not causes.

## Files
`01_ingest_clean.ipynb`, `rejected_rows.json`, `appointments_clean.csv`, `clinics_enriched.csv`, `load_data.sql`, `02_queries.sql`, `03_model.ipynb`, `test_risk_scores.csv`, `04_genai.ipynb` (key removed), `notes_analysed.csv`, `README.md`, `data/` (the three original files).
