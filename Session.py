import tkinter as tk
import csv
import numpy as np
from tkinter import *
import pandas as pd


class Session:
    def __init__(self, root, name, file, row):
        self.name = name
        self.file = file

        self.regular_check = IntVar()
        Checkbutton(root, text=f"{self.name}(x)", variable=self.regular_check).grid(
            row=row, column=0, sticky=W, padx=5, pady=5
        )

        self.first_der_check = IntVar()
        Checkbutton(root, text=f"{self.name}'(x)", variable=self.first_der_check).grid(
            row=row, column=1, sticky=W, padx=5, pady=5
        )

        self.second_der_check = IntVar()
        Checkbutton(
            root, text=f"{self.name}''(x)", variable=self.second_der_check
        ).grid(row=row, column=2, sticky=W, padx=5, pady=5)

        self.smooth_regular_check = IntVar()
        Checkbutton(root, text="Smooth", variable=self.smooth_regular_check).grid(
            row=row + 1, column=0, sticky=W, padx=5, pady=5
        )

        self.smooth_first_der_check = IntVar()
        Checkbutton(root, text="Smooth", variable=self.smooth_first_der_check).grid(
            row=row + 1, column=1, sticky=W, padx=5, pady=5
        )

        self.smooth_second_der_check = IntVar()
        Checkbutton(root, text="Smooth", variable=self.smooth_second_der_check).grid(
            row=row + 1, column=2, sticky=W, padx=5, pady=5
        )

        dataset = {"NanoTimestamp": [], "Channel0": [], "Channel1": []}

        # Parse the file
        with open(self.file, "r") as csvfile:
            csvreader = csv.reader(csvfile)

            for i, row in enumerate(csvreader):
                dataset["NanoTimestamp"].append(float(row[0]))
                dataset["Channel0"].append(float(row[1]))
                dataset["Channel1"].append(float(row[2]))

        # Shift timestamps toward 0
        start_time = dataset["NanoTimestamp"][0]
        dataset["NanoTimestamp"] = list(
            map(lambda n: n - start_time, dataset["NanoTimestamp"])
        )

        # Get the first derivative
        dataset["d_channel0"] = np.diff(dataset["Channel0"]) / np.diff(
            dataset["NanoTimestamp"]
        )
        dataset["d_timestamp"] = (
            np.array(dataset["NanoTimestamp"])[:-1]
            + np.array(dataset["NanoTimestamp"])[1:]
        ) / 2

        # Get the second derivative
        dataset["dd_channel0"] = np.diff(dataset["d_channel0"]) / np.diff(
            dataset["d_timestamp"]
        )
        dataset["dd_timestamp"] = (
            np.array(dataset["d_timestamp"])[:-1] + np.array(dataset["d_timestamp"])[1:]
        ) / 2

        # Get readable timestamps
        dataset["Timestamp"] = list(map(lambda n: n / 1e9, dataset["NanoTimestamp"]))
        dataset["DTimestamp"] = list(map(lambda n: n / 1e9, dataset["d_timestamp"]))
        dataset["DDTimestamp"] = list(map(lambda n: n / 1e9, dataset["dd_timestamp"]))

        self.timestamps = {
            "normal": dataset["Timestamp"],
            "first_der": dataset["DTimestamp"],
            "second_der": dataset["DDTimestamp"],
        }

        self.data = {
            "normal": dataset["Channel0"],
            "first_der": dataset["d_channel0"],
            "second_der": dataset["dd_channel0"],
        }

        # Setup smooth data
        df = pd.DataFrame({"y": self.data["normal"]}, index=self.timestamps["normal"])
        self.data["normal_smooth"] = df.rolling(2, win_type="gaussian").mean(std=3)

        df = pd.DataFrame(
            {"y": self.data["first_der"]}, index=self.timestamps["first_der"]
        )
        self.data["first_der_smooth"] = df.rolling(2, win_type="gaussian").mean(std=3)

        df = pd.DataFrame(
            {"y": self.data["second_der"]}, index=self.timestamps["second_der"]
        )
        self.data["second_der_smooth"] = df.rolling(2, win_type="gaussian").mean(std=3)
