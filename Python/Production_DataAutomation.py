import pandas as pd
import openpyxl
from datetime import datetime, timedelta
import sys

# ---------------------------------
# فایل‌ها
# ---------------------------------
INPUT_FILE = "daily analize.xlsm"
OUTPUT_FILE = "PPC - May.xlsx"

INPUT_SHEET = "daily analize"
OUTPUT_SHEET = "PPC"

START_ROW = 1674

OUTPUT_COLUMN = "G"
LEFT_COLUMN = "F"


# ---------------------------------
# مقادیر مقایسه
# ---------------------------------
limits = [
    280000,
    160000,
    600,
    240000,
    90000,
    120000,
    90000,
    140000,
    120000,
    120000,
    120000,
    120000,
    None
]

# ---------------------------------
# خواندن تاریخ از W1
# ---------------------------------
print("Reading W1...")

try:
    wb_temp = openpyxl.load_workbook(
        INPUT_FILE,
        data_only=True,
        read_only=True
    )

    ws_temp = wb_temp[INPUT_SHEET]
    date_cell = ws_temp["W1"].value
    wb_temp.close()

except Exception as e:
    print("ERROR reading W1:", e)
    sys.exit(1)

print("Raw W1 =", date_cell)

# ---------------------------------
# تبدیل تاریخ
# ---------------------------------
yesterday = (datetime.today() - timedelta(days=1)).date()

try:
    input_date = pd.to_datetime(date_cell).date()

except Exception as e:
    print("ERROR converting date:", e)
    sys.exit(1)

print("Date in file :", input_date)
print("Yesterday    :", yesterday)

# ---------------------------------
# خواندن داده‌ها
# ستون D = MACHINE
# ستون G = OUTPUT
# سطر 3 تا 39
# ---------------------------------
print("Reading rows 3 to 39...")

try:
    df = pd.read_excel(
        INPUT_FILE,
        sheet_name=INPUT_SHEET,
        usecols="D,G",
        skiprows=2,
        nrows=37,
        header=None
    )

    df.columns = ["MACHINE", "OUTPUT"]

except Exception as e:
    print("ERROR reading data:", e)
    sys.exit(1)

# حذف ردیف‌های خالی
df = df.dropna(subset=["MACHINE"])

# ---------------------------------
# اگر تاریخ برابر دیروز نبود
# ---------------------------------
if input_date != yesterday:
    print("Date mismatch -> OUTPUT = 0")
    df["OUTPUT"] = 0
else:
    print("Date matched -> using real outputs")

# ---------------------------------
# Group By
# ---------------------------------
grouped = (
    df.groupby("MACHINE", sort=False)["OUTPUT"]
    .sum()
    .reset_index()
)

# [تغییر اعمال شده برای رفع خطای LossySetitemError]
grouped["OUTPUT"] = grouped["OUTPUT"].astype(float)

# ---------------------------------
# تنظیم ترتیب ماشین‌ها
# ---------------------------------
grouped["MACHINE"] = pd.Categorical(
    grouped["MACHINE"],
    categories=machine_order,
    ordered=True
)

grouped = grouped.sort_values("MACHINE").reset_index(drop=True)

# ---------------------------------
# اصلاح مقادیر خاص (طبق درخواست جدید)
# ماشین 0 → تقسیم بر 0.7
# ماشین 2 → تقسیم بر 76
# ---------------------------------
if len(grouped) > 0:
    grouped.loc[0, "OUTPUT"] = grouped.loc[0, "OUTPUT"] / 0.7

if len(grouped) > 2:
    grouped.loc[2, "OUTPUT"] = grouped.loc[2, "OUTPUT"] / 76

print("\nGrouped Result:")
print(grouped)

# ---------------------------------
# باز کردن فایل خروجی
# ---------------------------------
print("\nOpening output file...")

try:
    wb_out = openpyxl.load_workbook(OUTPUT_FILE)
    ws_out = wb_out[OUTPUT_SHEET]

except Exception as e:
    print("ERROR opening output file:", e)
    sys.exit(1)

# ---------------------------------
# پیدا کردن اولین سطر خالی
# ---------------------------------
print("Finding first empty row...")

row = START_ROW

while ws_out[f"{OUTPUT_COLUMN}{row}"].value not in (None, ""):
    row += 1

print("First empty row =", row)

# ---------------------------------
# نوشتن داده‌ها
# ---------------------------------
values = grouped["OUTPUT"].tolist()

print(f"Writing {len(values)} values...")

for i, val in enumerate(values):

    current_row = row + i

    # ستون G
    ws_out[f"{OUTPUT_COLUMN}{current_row}"] = val

    # ستون F
    left_value = None

    if val != 0:

        limit = limits[i]

        if limit is None:
            left_value = val
        else:
            if val > limit:
                left_value = val
            else:
                left_value = limit

    ws_out[f"{LEFT_COLUMN}{current_row}"] = left_value

# ---------------------------------
# ذخیره فایل
# ---------------------------------
try:
    wb_out.save(OUTPUT_FILE)
    print("\nDONE ✅")
    print(f"Data written from row {row}")

except Exception as e:
    print("ERROR saving file:", e)
    print("Make sure Excel file is closed.")
