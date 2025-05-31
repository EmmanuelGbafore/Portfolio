import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind, pearsonr
import os

# Set your save directory
save_dir = "C:/Data Analyst Project"
os.makedirs(save_dir, exist_ok=True)

# Load cleaned and enriched data
reviews = pd.read_csv(f"{save_dir}/customer_reviews_enriched.csv")
customers = pd.read_csv(f"{save_dir}/dim_customer.csv")  # cleaned & includes AgeGroup
journey = pd.read_csv(f"{save_dir}/fact_customer_journey.csv")  # cleaned & formatted

# Merge reviews with customer demographics and journey info
df = reviews.merge(customers, on="CustomerID", how="left")
df = df.merge(journey, on="CustomerID", how="left")

# Drop rows with missing sentiment or age group
df = df.dropna(subset=["SentimentScore", "AgeGroup"])

# T-Test: Compare sentiment scores by AgeGroup (Young, Middle Age, Senior)
age_groups = df["AgeGroup"].unique()
print(f"Detected Age Groups: {age_groups}")

# Run pairwise t-tests (e.g. Young vs Middle Age, etc.)
group_pairs = [("Young", "Middle Age"), ("Young", "Senior"), ("Middle Age", "Senior")]

for g1, g2 in group_pairs:
    scores1 = df[df["AgeGroup"] == g1]["SentimentScore"]
    scores2 = df[df["AgeGroup"] == g2]["SentimentScore"]
    
    t_stat, p_val = ttest_ind(scores1, scores2, equal_var=False)
    print(f"T-test {g1} vs {g2}: t = {t_stat:.3f}, p = {p_val:.4f}")

# Save boxplot of sentiment by age group
plt.figure(figsize=(8, 5))
sns.boxplot(x="AgeGroup", y="SentimentScore", data=df, palette="Set2", order=["Young", "Middle Age", "Senior"])
plt.title("Sentiment Score by Age Group")
plt.savefig(f"{save_dir}/sentiment_by_age_group.png")
plt.close()

# Correlation: Sentiment vs Rating
df = df.dropna(subset=["Rating"])
corr, pval = pearsonr(df["SentimentScore"], df["Rating"])
print(f"Correlation between sentiment and rating: r = {corr:.3f}, p = {pval:.4f}")

# Save scatterplot
plt.figure(figsize=(8, 5))
sns.scatterplot(x="Rating", y="SentimentScore", data=df, alpha=0.6)
plt.title("Sentiment Score vs. Rating")
plt.savefig(f"{save_dir}/sentiment_vs_rating.png")
plt.close()
