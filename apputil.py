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

# creating visualize_demographic function


def visualize_demographic():

    results = survival_demographics()

    # Comparing pclass 1 men and pclass 3 women
    comparison = results[
        ((results["pclass"] == 1) & (results["sex"] == "male")) |
        ((results["pclass"] == 3) & (results["sex"] == "female"))
    ]

    # comparing across the different age groups
    comparison = (
        comparison
        .groupby("sex", observed=False)
        .agg(
            n_survivors=("n_survivors", "sum"),
            n_passengers=("n_passengers", "sum")
        )
        .reset_index()
    )

    comparison["survival_rate"] = (
        comparison["n_survivors"] / comparison["n_passengers"]
    )

    comparison["sex"] = comparison["sex"].replace({
        "female": "Third Class Women",
        "male": "First Class Men"
    })

    fig = px.bar(
        comparison,
        x="sex",
        y="survival_rate",
        title="Survival Rate of Third-Class Women vs First-Class Men",
        labels={
            "sex": "Sex",
            "survival_rate": "Survival Rate"
        },
        color="sex",
        color_discrete_map={
            "Third Class Women": "pink",    # basic boy girl colors lol
            "First Class Men": "blue"
        }
    )

    fig.update_layout(showlegend=False)

    return fig
