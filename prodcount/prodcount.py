import csv
from pprint import pprint
from collections import defaultdict


productive = ["Work", "Self growth", "Build"]
drain = ["Family", "Friends", "Errand", "LifePlan"]
leisure = ["Waste", "Meals"]


def calculate_hours(row, out_row):
    # Aggregate
    if row["Classification 1"] in productive:
        out_row["Productive hours"] += int(row["Number of hours"])
    if row["Classification 1"] in drain:
        out_row["Drain hours"] += int(row["Number of hours"])
    if row["Classification 1"] in leisure:
        out_row["Leisure hours"] += int(row["Number of hours"])

    out_row["Total hours"] += (
        int(row["Number of hours"]) if row["Number of hours"] != "" else 0
    )

    # Calculate percentages
    out_row["% Productive"] = round(
        (out_row["Productive hours"] / out_row["Total hours"]) * 100, 2
    )
    out_row["% Drained"] = round(
        (out_row["Drain hours"] / out_row["Total hours"]) * 100, 2
    )
    out_row["% Leisure"] = round(
        (out_row["Productive hours"] / out_row["Total hours"]) * 100, 2
    )
    return out_row


def main():
    print("Enter input filename(optionally with path):")
    input_filepath = str(input())
    print("Enter output filename(optionally with path):")
    output_filepath = str(input())


    with open(input_filepath) as f:
        reader = csv.DictReader(f, delimiter=",")
        data = list(reader)
        out = []

        for row in data:
            for out_row in out:
                if row["Date"] == out_row["Date"]:
                    out_row = calculate_hours(row, out_row)
                    break
            else:
                # For empty
                if row["Date"] != "":
                    out.append(
                        {
                            "Date": row["Date"],
                            "Total hours": int(row["Number of hours"])
                            if row["Number of hours"] != ""
                            else 0,
                            "Productive hours": int(row["Number of hours"])
                            if row["Classification 1"] in productive
                            else 0,
                            "Drain hours": int(row["Number of hours"])
                            if row["Classification 1"] in drain
                            else 0,
                            "Leisure hours": int(row["Number of hours"])
                            if row["Classification 1"] in leisure
                            else 0,
                        }
                    )

    with open(output_filepath, "w") as outf:
        writer = csv.DictWriter(outf, out[0].keys())
        writer.writeheader()
        writer.writerows(out)

    print("Done!")


if __name__ == "__main__":
    main()
