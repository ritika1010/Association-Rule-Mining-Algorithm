# Association-Rule-Mining-Algorithm

## Team
- Ritika Deshpande (rgd2127)
- Nagavasavi Jeepalyam (nj2506)

## (a) List of files submitted
- proj3.tar.gz file with the project code
- INTEGRATED_DATASET.csv
- README
- output.txt

## (b) Running Project on the Cloud

- **Install dependencies**
    - pip3 install numpy
    - pip3 install pandas

- **Run**
    - python3 algo.py INTEGRATED-DATASET.csv 0.01 0.5

## (c) About the Data

**Dataset Used**: [New York City Leading Causes of Death](https://data.cityofnewyork.us/Health/New-York-City-Leading-Causes-of-Death/jb7j-dtam/about_data)

### Dataset Modification Procedure

The original dataset contained *1094* rows of data, where each row described details about a popular baby name. There were 7 columns:

1. **year**
2. **Leading Cause**
3. **Sex** (The decedent's sex)
4. **Race Ethnicity** (The decedent's ethnicity)
5. **Deaths** (The number of people who died due to cause of death)
6. **Death Rate** (The death rate within the sex and Race/ethnicity category)
7. **Age Adjusted Death Rate** (The age-adjusted death rate within the sex and Race/ethnicity category)