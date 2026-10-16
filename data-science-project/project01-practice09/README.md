# US Community Environmental Safety & Public Health Analysis
## Problem / Research Question
How does community‑level housing insecurity relate to adult depression prevalence across counties in the United States? This project explores whether counties with higher housing insecurity show higher rates of adult depression.

## Dataset source and usage permissions
Dataset source: CDC PLACES 2024 County‑level public health dataset from Centers for Disease Control and Prevention (CDC).
Download link: https://data.cdc.gov/api/v3/views/eav7‑hnsx/export.csv?accessType=DOWNLOAD
License: Public Domain (CC0). This is anonymized aggregated county‑level statistics. No individual personal data, passwords, API keys or restricted information are included in the dataset.
The raw dataset is provided in long‑form format, where each row stores one health indicator for a given county.

## Methods and tools used
Python, Pandas for data cleaning and data reshaping, Matplotlib and Seaborn for visualization.
Steps:
1. Load the raw `export.csv` dataset
2. Filter dataset to retain two target indicators: housing insecurity and adult depression
3. Reshape long‑format data into wide‑format table using pivot operation
4. Remove records containing missing values
5. Compute Pearson correlation coefficient between housing insecurity and depression
6. Create two visualizations: correlation heatmap and state‑level depression prevalence bar chart

## Key findings and one limitation
**Key findings**: The Pearson correlation coefficient between county‑level housing insecurity and adult depression prevalence is only 0.02, which suggests nearly no linear correlation between these two variables in this dataset. When aggregated to state level, southern US states including Mississippi, New Mexico and Louisiana show the highest average adult depression prevalence.

**Limitation**: This dataset is aggregated county‑level cross‑sectional data. We can only observe statistical correlation and cannot establish causal relationships. Important confounding factors such as household income, education level and local mental‑health service resources are not controlled in this simple analysis.

## Instructions for running the analysis
1. Clone this repository locally
2. Install dependencies: `pip install -r requirements.txt`
3. Download the CDC csv file from the provided URL and save it as `export.csv` inside the `project01‑practice09` folder
4. Navigate into the `project01‑practice09` folder and run `community_health_analysis.py` in your Python environment
5. Generated visualization images will be saved into the `visualizations/` sub‑folder

## Visualizations
### 1. Correlation Heatmap
![Correlation Heatmap](project01‑practice09/visualizations/correlation_heatmap.png)
The Pearson correlation coefficient between housing insecurity and adult depression is 0.02, indicating **nearly no linear correlation** between these two variables in this county‑level dataset.

### 2. Top 10 States by Adult Depression Prevalence
![Depression Bar Chart](project01‑practice09/visualizations/state_bar.png)
Mississippi has the highest average adult depression rate among the top 10 states, followed by New Mexico and Louisiana.

## Conclusion
There is almost no linear association between county‑level housing insecurity and adult depression prevalence based on this CDC PLACES dataset. Higher adult depression prevalence is concentrated across southern US states. Further analysis incorporating socioeconomic confounding variables would help to better understand drivers of depression at community level.
