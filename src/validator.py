import pandas as pd


def load_data(file_path):
    return pd.read_csv(file_path)


def find_missing_values(df):
    return df.isnull().sum()


def find_duplicate_records(df):
    return df[df.duplicated(keep=False)]


def find_duplicate_customer_ids(df):
    return df[df.duplicated(subset=["customer_id"], keep=False)]

def find_missing_data_records(df):
    missing_mask = df.isnull().any(axis=1)
    result = df[missing_mask].copy()
    result["missing_columns"] = df[missing_mask].apply(
        lambda row: list(df.columns[row.isnull()]), axis=1
    )
    return result

def generate_validation_summary(df):
    total_records = len(df)
    total_columns = len(df.columns)

    records_with_missing_data = int(df.isnull().any(axis=1).sum())

    duplicate_customer_ids = int(
        df.loc[df["customer_id"].duplicated(keep=False), "customer_id"]
        .nunique()
    )

    status = "FAILED" if (
        records_with_missing_data > 0 or duplicate_customer_ids > 0
    ) else "PASSED"

    return {
        "total_records": total_records,
        "total_columns": total_columns,
        "records_with_missing_data": records_with_missing_data,
        "duplicate_customer_ids": duplicate_customer_ids,
        "status": status
    }


if __name__ == "__main__":
    file_path = "data/customers.csv"

    df = load_data(file_path)

    print("\n=== CUSTOMER DATA ===")
    print(df)

    print("\n=== DUPLICATE RECORDS ===")
    duplicate_records = find_duplicate_records(df)
    print(duplicate_records)

    print("\n=== MISSING DATA RECORDS ===")
    missing_data_records = find_missing_data_records(df)
    print(missing_data_records)

    summary = generate_validation_summary(df)
    print(summary)
    # print("\n=== MISSING VALUES ===")
    # print(find_missing_values(df))

    # print("\n=== DUPLICATE RECORDS ===")
    # print(find_duplicate_records(df))

    # print("\n=== DUPLICATE CUSTOMER IDs ===")
    # print(find_duplicate_customer_ids(df))