1. **Meta-features Extraction**:
    - From the whole raw data, meta-features are extracted.

2. **Normalization**:
    - The raw data is split into a train set and a test set.
    - Both splits are then normalized through z-score.

2. **Training**:
    - A `LogisticRegressor()` scorer is trained for the Quantifiers, using the train set.
    - The Quantifiers are evaluated through APP, using the test set.

3. **Meta-table Generation**:
    - With the Meta-table and the Quantifiers' performance (estimated with APP), we generate the Meta-table.

4. **Recommendation System Training**:
    - Using the Meta-table, we train the Recommendation system using `Support Vector Regressor (SVR)`.