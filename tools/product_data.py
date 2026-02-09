import pandas as pd

DATA_PATH = "data/dataset.csv"

def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)

    df["order_key"] = (
        df["Customer_Id"].astype(str)
        + "_" + df["Order_Date"]
        + "_" + df["Time"]
    )

    return df