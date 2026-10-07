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

    comparison["sex"] = comparison["sex"].replace({     # Changing the x-axis name for readability
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


# exercise two in family_groups
def family_groups():
    # defining family size. we need siblings plus all of the parents
    df["family_size"] = df["sibsp"] + df["parch"] + 1

    # next we are finding the answers for part two
    result = (
        df.groupby(["pclass", "family_size"])
        .agg(
            n_passengers=("passengerid", "count"),
            avg_fare=("fare", "mean"),
            min_fare=("fare", "min"),
            max_fare=("fare", "max")
        )
        .reset_index()
        .sort_values(["pclass", "family_size"])
    )

    return result


family_groups()

# next we need to find last names


def last_names():
    names = df["name"].str.split(",").str[0]
    return names.value_counts()

# Now making second graph for visualize_families


def visualize_families():
    df["last_name"] = df["name"].str.split(",").str[0]
    df["family_size"] = df["sibsp"] + df["parch"] + 1

    families = (
        df.groupby(["last_name", "family_size"])
        .agg(
            survivors=("survived", "sum"),
            passengers=("survived", "count")
        )
        .reset_index()
    )

    families = families[
        (families["family_size"] > 3) &
        (families["survivors"] == 1)
    ]

    families = families.sort_values("family_size", ascending=False)

    fig = px.bar(
        families,
        x="last_name",
        y="family_size",
        color="family_size",
        text="family_size",
        color_continuous_scale="Viridis",
        title="Families Larger Than Three Members With One Survivor",
        labels={
            "last_name": "Family",
            "family_size": "Family Size"
        }
    )

    fig.update_layout(showlegend=False)

    return fig
