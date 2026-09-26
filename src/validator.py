import os
import pandas as pd


def load_data(file_path):
    return pd.read_csv(file_path)


def find_missing_values(df):
    return df.isnull().sum()


def find_missing_data_records(df):
    return df[df.isnull().any(axis=1)]


def find_duplicate_records(df):
    return df[df.duplicated(keep=False)]


def find_duplicate_customer_ids(df):
    return df[df.duplicated(subset=["customer_id"], keep=False)]


def generate_validation_summary(df):
    total_records = len(df)
    total_columns = len(df.columns)

    records_with_missing_data = df.isnull().any(axis=1).sum()
    duplicate_customer_ids = int(
    df.loc[
        df["customer_id"].duplicated(keep=False),
        "customer_id"
    ].nunique()
)

    return {
        "total_records": total_records,
        "total_columns": total_columns,
        "records_with_missing_data": records_with_missing_data,
        "duplicate_customer_ids": duplicate_customer_ids
    }


def generate_validation_report(df, file_name):
    summary = generate_validation_summary(df)
    missing_records = find_missing_data_records(df)
    duplicate_records = find_duplicate_customer_ids(df)

    status = "FAILED" if (summary["records_with_missing_data"] > 0
                           or summary["duplicate_customer_ids"] > 0) else "PASSED"

    # Build "Missing <column> -> Customer <id>" lines
    issue_lines = []
    for _, row in missing_records.iterrows():
        customer_id = row["customer_id"]
        missing_cols = row[row.isnull()].index.tolist()
        for col in missing_cols:
            issue_lines.append((f"Missing {col}", customer_id))

    # Build "Duplicate ID -> Customer <id>" lines
    # keep="first" marks only the *extra* occurrences as duplicates,
    # matching the count already used in generate_validation_summary
    dup_mask = df["customer_id"].duplicated(keep="first")
    for customer_id in df.loc[dup_mask, "customer_id"]:
        issue_lines.append(("Duplicate ID", customer_id))

    # Align the "Missing x -> Customer y" labels into columns
    label_width = max((len(label) for label, _ in issue_lines), default=0)
    issue_text = "\n".join(
        f"{label:<{label_width}} \u2192 Customer {cid}" for label, cid in issue_lines
    ) if issue_lines else "None"

    width = 40
    report = (
        f"{'=' * width}\n"
        f"{'BUSINESS DATA VALIDATION'.center(width)}\n"
        f"{'=' * width}\n\n"
        f"File: {file_name}\n\n"
        f"SUMMARY\n"
        f"{'-' * width}\n"
        f"{'Total Records':<24}: {summary['total_records']}\n"
        f"{'Total Columns':<24}: {summary['total_columns']}\n"
        f"{'Missing Data Records':<24}: {summary['records_with_missing_data']}\n"
        f"{'Duplicate Customer IDs':<24}: {summary['duplicate_customer_ids']}\n\n"
        f"STATUS\n"
        f"{'-' * width}\n"
        f"{status}\n\n"
        f"ISSUES\n"
        f"{'-' * width}\n"
        f"{issue_text}\n"
    )

    os.makedirs("reports", exist_ok=True)
    report_path = os.path.join("reports", f"{os.path.splitext(file_name)[0]}_report.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)

    return report


if __name__ == "__main__":
    file_path = "data/customers_duplicates.csv"
    file_name = os.path.basename(file_path)

    df = load_data(file_path)

    print("\n=== CUSTOMER DATA ===")
    print(df)

    report = generate_validation_report(df, file_name)
    print("\n" + report)

    # Individual pieces are still available if you want them separately:
    # print("\n=== MISSING VALUES ===")
    # print(find_missing_values(df))

    # print("\n=== MISSING DATA RECORDS ===")
    # print(find_missing_data_records(df))

    # print("\n=== DUPLICATE RECORDS ===")
    # print(find_duplicate_records(df))

    # print("\n=== DUPLICATE CUSTOMER IDs ===")
    # print(find_duplicate_customer_ids(df))