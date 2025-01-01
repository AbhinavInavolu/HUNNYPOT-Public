import pandas as pd
import scipy as sp
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import scikit_posthocs as sph


df1 = pd.read_csv(r'analysis\parsed\all.csv')
df2 = pd.read_csv(r'analysis\parsed\unique.csv')

# Remove org type
merged_df1 = df1.copy()
merged_df2 = df2.copy()
merged_df1['Config'] = merged_df1['Config'].str.split('_', n=1).str[1]
merged_df2['Config'] = merged_df2['Config'].str.split('_', n=1).str[1]

pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

org_configs = [
    "restaurant_high_high", "restaurant_high_low", "restaurant_low_high", "restaurant_low_low",
    "hospital_high_high", "hospital_high_low", "hospital_low_high", "hospital_low_low",
    "bank_high_high", "bank_high_low", "bank_low_high", "bank_low_low"
]

cpu_ram_configs = ["high_high", "high_low", "low_high", "low_low"]

org_dfs = [df1[df1.Config == config] for config in org_configs]
unique_org_dfs = [df2[df2.Config == config] for config in org_configs]
merged_dfs = [merged_df1[merged_df1.Config == config] for config in cpu_ram_configs]
unique_merged_dfs = [merged_df2[merged_df2.Config == config] for config in cpu_ram_configs]

def run_anova_with_tukey(df, val_col, two_way):
    print("### ANOVA ###")
    if two_way:
        model = ols(f'{val_col} ~ C(RAM) * C(CPU)', data=df).fit()
        df["interaction"] = df['RAM'].astype(str) + "_" + df['CPU'].astype(str)
    else:
        model = ols(f'{val_col} ~ C(Organization) * C(RAM) * C(CPU)', data=df).fit()
        df["interaction"] = df['Organization'].astype(str) + "_" + df['RAM'].astype(str) + "_" + df['CPU'].astype(str)

    anova_table = sm.stats.anova_lm(model, typ=2)
    print(anova_table)

    if min(anova_table["PR(>F)"]) < 0.1:
        print("\n### Tukey ###")
        print(pairwise_tukeyhsd(endog=df[val_col], groups=df["interaction"], alpha=0.1))

def run_kruskal_with_dunn(dfs, df, val_col):
  print("\n### Kruskal Wallis ###")
  h_statistic, p_value = sp.stats.kruskal(*[df[val_col] for df in dfs])
  print(f"H-statistic: {h_statistic}, P-value: {p_value:.4f}")

  if p_value < 0.1:
    results = sph.posthoc_dunn(df, val_col=val_col, group_col="Config")

    for i in range(0, results.shape[1], 6):
        print(results.iloc[:, i:i+6])

def run_tests(dfs, df_for_posthoc, label):
  print(f"######### {label} #########")

  for val_col in ('Duration_Seconds', 'Num_Commands'):
    print(f"###### {val_col} ######")

    run_anova_with_tukey(df_for_posthoc, val_col, 'Org' not in label)
    run_kruskal_with_dunn(dfs, df_for_posthoc, val_col)

    print("\n")

test_groups = [
  (org_dfs, df1, 'All Org'),
  (unique_org_dfs, df2, 'Unique Org'),
  (merged_dfs, merged_df1, 'All Merged'),
  (unique_merged_dfs, merged_df2, 'Unique Merged')
]

for dfs, df_for_posthoc, label in test_groups:
  run_tests(dfs, df_for_posthoc, label)
  print("\n\n")




