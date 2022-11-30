import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("predicted_corrosion.csv")

# select_category is always categorical
select_category = ["Well Name"]  # Maximum 1

# select_sub_category is always categorical
select_sub_categiory = []  # Maximum 1
# y are always numeric
select_series = ["Pred_by 7in", "Pred_by 10in", "Pred_by 13in"]  # y is always numeric
operation = "sum"  # defult is count and user can't select operation without selecting the select_series
if len(select_series) < 1:
    output = pd.DataFrame(df[select_category + select_sub_categiory].value_counts())
    output = output.rename(columns={0: "select_series"})
    output = output.reset_index()
    print(output)

    if len(select_sub_categiory) > 0:
        output = pd.pivot_table(output, index=select_category, columns=select_sub_categiory, values="select_series",
                                aggfunc="sum")
        # output.columns = output.columns.map(lambda x: '_'.join([str(i) for i in x]))
        output = output.reset_index()
        output = output.fillna(0)
else:
    output = df[select_category + select_sub_categiory + select_series]
    output = pd.pivot_table(output, index=select_category, columns=select_sub_categiory, values=select_series,
                            aggfunc=operation)
    if len(select_sub_categiory) > 0:
        output.columns = output.columns.map(lambda x: '_'.join([str(i) for i in x]))
    output = output.reset_index()
    output = output.fillna(0)

trace_dict = {}
for col in output.columns[1:]:
    trace_dict.update({col: {"x": output[select_category[0]].values.tolist(), "y": output[col].values.tolist()}})

print(trace_dict)
