# Association-Rule-Mining-Algorithm

## (a) Team
- Ritika Deshpande (rgd2127)
- Nagavasavi Jeepalyam (nj2506)

## (b) List of files submitted
- proj3.tar.gz file with the project code
    - algo.py
    - clean_data.py
- INTEGRATED-DATASET.csv
- README
- example-run.txt

## (c) Running Project on the Cloud

- **Install dependencies**
    - pip3 install numpy
    - pip3 install pandas

- **Run**
    - python3 algo.py INTEGRATED-DATASET.csv 0.01 0.5

## (d) Dataset Description

- **(a)Dataset Used**: [New York City Leading Causes of Death](https://data.cityofnewyork.us/Health/New-York-City-Leading-Causes-of-Death/jb7j-dtam/about_data) 
   The original dataset contained *1094* rows of data and provides information about deaths in New York City and includes various attributes such as age, sex, race, cause of death, and borough. There were 7 columns:
    1. **year**
    2. **Leading Cause**
    3. **Sex** (The decedent's sex)
    4. **Race Ethnicity** (The decedent's ethnicity)
    5. **Deaths** (The number of people who died due to cause of death)
    6. **Death Rate** (The death rate within the sex and Race/ethnicity category)
    7. **Age Adjusted Death Rate** (The age-adjusted death rate within the sex and Race/ethnicity category)
 
- **(b) Dataset Modification Procedure**
    1. Data Retrieval: Initially, we accessed the "NYC_Deaths" data set from the NYC Open Data website (insert link to the data set).
    2. Data Cleaning:
        - Duplicate Removal: We removed duplicate records from the data set to ensure data integrity and eliminate redundancy.
        - Handling Missing Values: Rows with missing values (NA values) were removed from the data set to ensure completeness and accuracy.
        - Value Standardization: Values in the 'Sex' column were standardized by replacing 'F' and 'M' with 'Female' and 'Male' respectively, for better clarity and consistency.
    3. Data Integration: After cleaning the data, we integrated the relevant attributes into a single CSV file named 'INTEGRATED-DATA.csv', formatted according to the project requirements

- **(c) Justification for Data Set Choice:**
    The choice of the "NYC_Deaths" data set was made based on several factors:

    - **Relevance:** The data set contains vital information about deaths in New York City, which is relevant for various analyses and insights.
    - **Availability of Attributes:** It provides a wide range of attributes such as age, sex, and cause of death, allowing for comprehensive analysis.
    - **Potential for Association Rule Mining:** The diversity of attributes presents opportunities to extract meaningful association rules that could offer insights into mortality trends and patterns.

## (e) Internal design of the project:
The code implements the Apriori algorithm, a classic algorithm for association rule mining, to identify frequent itemsets and high-confidence association rules from transactional data. The implementation includes variations to optimize performance and adapt to specific requirements.

### Components:
1. **Algorithm Implementation:**
    The Apriori algorithm is implemented to generate frequent itemsets and association rules.
    Variations in the algorithm optimize support calculation and association rule generation.
2. **Database Management:**
    SQLite database is used to manage data storage and manipulation.
    Dynamic table creation is employed to store candidate itemsets and support values during algorithm execution.
3. **File I/O Operations:**
    Input data is read from a CSV file, and results are written to an output text file.
    Command-line arguments are used to specify minimum support and confidence thresholds.

### Detailed Procedure:
1. **Table Creation:**
    Tables for candidate itemsets (L1, L2, L3, C2, C3, C4) are created using SQL CREATE statements.
    These tables are used to store itemsets and support values during the algorithm execution.
2. **Database Connection:**
    SQLite database connection is established, and a cursor is created for executing SQL queries.
3. **Data Reading:**
    Transactional data is read from a CSV file specified as a command-line argument.
    Each row of the CSV file represents a transaction.
4. **Preprocessing:**
    Data preprocessing involves cleaning and formatting the input data.
    Invalid or incomplete rows are skipped, and numerical values are extracted for support calculation.
5. **Support Calculation:**
    The algorithm calculates the support for each item and identifies frequent items (L1) based on the minimum support threshold.
6. **Candidate Generation:**
    The algorithm generates candidate itemsets of higher orders (C2, C3, C4) from frequent itemsets of lower orders (L1, L2, L3).
7. **Support Pruning:**
    Candidate itemsets are pruned based on the minimum support threshold.
8. **Association Rule Generation:**
    High-confidence association rules are generated from frequent itemsets.
    Association rules are filtered based on the minimum confidence threshold.
9. **Output Generation:**
    Results, including frequent itemsets and association rules, are written to an output text file.
    The output file contains detailed information about frequent itemsets and association rules, along with their support and confidence values.

### Variations:
1. Dynamic Table Creation: Tables are created dynamically based on the size of itemsets to optimize database operations and storage.
2. Efficient Support Calculation: Support values are computed incrementally to minimize computational overhead.
3. Association Rule Filtering: Variations in association rule generation enable the extraction of high-confidence association rules based on user-defined thresholds.

### Justification:
1. Scalability: The implementation is designed to handle large transactional datasets efficiently, making it suitable for real-world applications.
2. Customizability: Variations in the algorithm allow adaptation to specific requirements and optimization based on dataset characteristics.
3. Performance Optimization: Techniques such as dynamic table creation and efficient support calculation contribute to improved performance and reduced complexity.

## (f) Sample run:
- python3 algo.py INTEGRATED-DATASET.csv 0.001 0.5
- The result looks interesting as from the data we can find that the death cause is prominent for some genders and some ethnicity.
    - (death cause) → (gender)
    - (death cause) → (ethnicity)
    - (ethnicity) → (gender)
    - (year, ethnicity) → (gender)

**Examples:** 
- ('human immunodeficiency virus disease (hiv: b20-b24)',) ===> ('male',)	 conf: 66.83% 	 supp: 1.44%
- ('human immunodeficiency virus disease (hiv: b20-b24)',) ===> ('black non-hispanic',)	 conf: 65.91% 	 supp: 1.42%
- ('diabetes mellitus (e10-e14)',) ===> ('female',)	 conf: 52.38% 	 supp: 2.86%



