import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def line_format(label):
    """
    Convert time label to the format of pandas line plot
    """
    lab = label.month_name()[:3]
    if lab == "Jan":
        lab += f"\n{label.year}"
    if lab == "Feb" and label.year == 2019:
        lab = f"\n{label.year}"
    return lab


def generic_graph_settings():
    xlim = ax.get_xlim()
    ax.fill_between(xlim, 0, 5, color="#e6b5bf", zorder=10)
    ax.grid(b=False)
    ax.set_title(title, loc="left")
    ax.set_xlim(xlim)
    ax.set_ylim(ymin=0)
    ax.set_ylabel("Count of repeated positive tests")
    plt.tight_layout()


## Get data
df = pd.read_csv(
    "output/input.csv",
    index_col="patient_id",
    parse_dates=["first_positive_date", "last_positive_date"],
)
time_between_positives = (df["last_positive_date"] - df["first_positive_date"]).dt.days
df = df.loc[time_between_positives > 90]
time_between_positives = time_between_positives.loc[time_between_positives > 90]
bins = np.arange(0, 420, 30)
ax = time_between_positives.hist(bins=bins, zorder=0)
title = "Time between first and last positive test"
ax.set_xlabel("Time since first positive test (days)")
generic_graph_settings()
plt.savefig("output/interval_between_positives.svg")

##
monthly_counts = (
    df.set_index("last_positive_date")["subsequent_positive"].resample("M").count()
)
ax = monthly_counts.plot(kind="bar", width=1, zorder=0)
title = "Month of repeated positive"
ax.set_xticklabels(map(line_format, monthly_counts.index), rotation="horizontal")
ax.xaxis.label.set_visible(False)
generic_graph_settings()
plt.savefig("output/repeated_positive_date.svg")
plt.close()
