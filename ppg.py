#!/bin/python

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import csv
import sys
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import *
import Session
from Session import Session


def show_graphs(datasets):
    data = {"x": [], "y": []}
    for sets in datasets:
        if sets["session"].regular_check.get() == 1:
            data["y"].append(sets["session"].data["normal"])
            data["x"].append(sets["session"].timestamps["normal"])
        if sets["session"].first_der_check.get() == 1:
            data["y"].append(sets["session"].data["first_der"])
            data["x"].append(sets["session"].timestamps["first_der"])
        if sets["session"].second_der_check.get() == 1:
            data["y"].append(sets["session"].data["second_der"])
            data["x"].append(sets["session"].timestamps["second_der"])
        if sets["session"].smooth_regular_check.get() == 1:
            data["y"].append(sets["session"].data["normal_smooth"])
            data["x"].append(sets["session"].timestamps["normal"])
        if sets["session"].smooth_first_der_check.get() == 1:
            data["y"].append(sets["session"].data["first_der_smooth"])
            data["x"].append(sets["session"].timestamps["first_der"])
        if sets["session"].smooth_second_der_check.get() == 1:
            data["y"].append(sets["session"].data["second_der_smooth"])
            data["x"].append(sets["session"].timestamps["second_der"])

    fig, ax = plt.subplots(figsize=(8, 6))
    plt.axhline(0, color="green")
    plt.axvline(0, color="green")

    for i in range(len(data["x"])):
        ax.plot(data["x"][i], data["y"][i])

    plt.show()


window = tk.Tk()
window.title("Graph Builder")

Label(window, text="Choose data:").grid(row=0, sticky=W, padx=5, pady=5)

datasets = [
    {
        "name": "20_hz",
        "file": "data/20hz_ppg.csv",
    },
    {
        "name": "30_hz",
        "file": "data/30hz_ppg.csv",
    },
    {
        "name": "60_hz",
        "file": "data/60hz_ppg.csv",
    },
    {
        "name": "100_hz",
        "file": "data/100hz_ppg.csv",
    },
]

for i in range(len(datasets)):
    datasets[i]["session"] = Session(
        window, datasets[i]["name"], datasets[i]["file"], (i * 2) + 1
    )

last_row = (len(datasets) * 2) + 1
Button(window, text="Show", command=lambda: show_graphs(datasets)).grid(
    row=last_row, column=0, padx=10, pady=10
)

window.mainloop()
