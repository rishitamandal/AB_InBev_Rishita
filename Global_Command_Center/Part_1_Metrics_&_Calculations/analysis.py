import pandas as pd

# Load the datasets
actuals_df = pd.read_csv('actuals.csv')
target_df = pd.read_csv('targets.csv')
price_df = pd.read_csv('price.csv')
bcr_df = pd.read_csv('bottle_crate.csv')

# Clean the datasets (if needed)

# Merge datasets to create a consolidated view of Actuals data
consolidated_df = actuals_df.merge(price_df, on=['Material Number'])
consolidated_df = consolidated_df.merge(bcr_df, on=['Material Number', 'Plant'])

# Calculate Bottle Rands and Crate Rands
consolidated_df['Bottle Rands'] = consolidated_df['Bottle Price'] * consolidated_df['Bottle Quantity']
consolidated_df['Crate Rands'] = consolidated_df['Crate Price'] * consolidated_df['Crate Quantity']

# Variance analysis: Actuals vs Target by Plant
variance_df = actuals_df.merge(target_df, on=['Material Number', 'Plant', 'Period', 'Year'])
variance_df['Quantity Variance'] = variance_df['Actuals'] - variance_df['Target']

# Variance analysis: Actuals, Target, and their variance by Plant and Category
variance_category_df = consolidated_df.merge(target_df, on=['Material Number', 'Plant', 'Period', 'Year'])
variance_category_df['Quantity Variance'] = variance_category_df['Actuals'] - variance_category_df['Target']

# Trend analysis for each Category and Plant (assuming monthly data)
trend_analysis = consolidated_df.groupby(['Category', 'Plant']).agg({'Actuals': 'mean'}).reset_index()

# Focus areas and planning periods
focus_areas = variance_category_df.groupby(['Plant', 'Category']).agg({'Quantity Variance': 'sum'}).reset_index()
planning_periods = trend_analysis.groupby(['Category', 'Plant']).agg({'Actuals': 'idxmax'}).reset_index()

# Print the results or perform further analysis as needed
print("Consolidated Actuals Data:")
print(consolidated_df)

print("\nVariance Analysis (Actuals vs Target) by Plant:")
print(variance_df)

print("\nVariance Analysis (Actuals, Target, and Variance) by Plant and Category:")
print(variance_category_df)

print("\nTrend Analysis for each Category and Plant:")
print(trend_analysis)

print("\nFocus Areas (Plant, Category) for Improvement:")
print(focus_areas)

print("\nPlanning Periods (Category, Plant) with Highest Actuals:")
print(planning_periods)
