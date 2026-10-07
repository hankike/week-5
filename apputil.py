import plotly.express as px
import pandas as pd

# update/add code below ...
# downloading dataset and cleaning column names
df = pd.read_csv(
    'https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')

df.columns = (
    df.columns
    .str.lower()
    .str.replace(" ", "_")
)
# exercise one in surival_demographics


def survival_demographics():

    # Creating age groups
    df["age_group"] = pd.cut(
        df["age"],
        bins=[0, 12, 19, 60, float("inf")],
        labels=["Child", "Teen", "Adult", "Senior"],
        right=False
    )

    # Grouping by pclass, sex, and age_group
    results = (
        df.groupby(
            ["pclass", "sex", "age_group"],
            observed=False
        )
        # find n_passengers and n_survived
        .agg(
            n_passengers=("survived", "size"),
            n_survivors=("survived", "sum")
        )
        .reset_index()
    )

    # find survival_rate
    results["survival_rate"] = (
        results["n_survivors"] / results["n_passengers"]
    )

    return results
