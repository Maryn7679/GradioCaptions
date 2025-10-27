import pandas as pd

df = pd.DataFrame()
df2 = pd.DataFrame()

df['Name'] = ['Anna', 'Pete', 'Tommy']
df['Scores'] = [97, 600, 200]

df2['Name'] = ['Anna', 'Pete', "None"]
df2['Scores'] = [97, 601, None]

# print(df)
# print(df2)
# df["Name"].loc[
#             df2["Scores"] != df["Scores"]
#                                 ] = "Test"
print(df2["Scores"] != df["Scores"])
