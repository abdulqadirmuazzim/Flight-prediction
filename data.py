import pandas as pd
import numpy as np

data = pd.read_excel("Data_Train.xlsx").dropna()

routes = data.Route.value_counts()

rare_routes = routes[routes < 100].index.to_list()

# ROUTES
route_list = (
    data.Route.apply(lambda x: "Other" if x in rare_routes else x).unique().tolist()
)

# SOURCES
sources = data.Source.unique().tolist()
# DESTINATIONS
destinations = data.Destination.unique().tolist()

# -----ADDITIONAL INNFORMATION-----

# correct the spelling issue
data["Additional_Info"] = data.Additional_Info.str.lower()

# get the counts of each unique value
info = data.Additional_Info.value_counts()
# get counts less than 100
rare_info = info[info < 100].index.to_list()

data["Additional_Info"] = data.Additional_Info.apply(
    lambda x: "Other" if x in rare_info else x
)
additional_info = data.Additional_Info.unique().tolist()
# ---AIRLINE---

airline = data.Airline.unique().tolist()
airline.remove("Trujet")


def filter_routes(source, destination, routes=route_list):
    """
    Returns the data for a specific route.
    """
    route = data.loc[data.Source == source]["Route"].iloc[0]
    dest = data.loc[data.Destination == destination]["Route"].iloc[0]

    src = route.split("→")[0].strip()
    dest = dest.split("→")[-1].strip()

    route_list = []

    for r in routes:
        r = str(r)
        if r.startswith(src) and r.endswith(dest):
            route_list.append(r)

    return route_list if route_list else ["Other"]
