import argparse
import hashlib
import pandas as pd
import re

##  aws configure
##  aws s3 cp ~/Desktop/CRM_data.csv  s3://com.dy-external.crm/f62ab5d26b23089ea3b5d52a07f39e25/upload_2024-05-13_00-00/CRM_data.csv

# https://support.dynamicyield.com/hc/en-us/articles/360021867314-User-Data-Onboarding-by-CSV
# https://support.dynamicyield.com/hc/en-us/community/posts/360014412458-Uploading-CRM-file-to-s3-bucket-using-CLI

# python3 csv-hasher.py ~/Desktop/hubspot-crm-exports-2024-04-19-icu-for-tri-weekly-s-2024-05-09.csv ~/Desktop/CRM_data2.csv Email -a sha256
# s3://com.dy-external.crm/f62ab5d26b23089ea3b5d52a07f39e25/upload_2024-05-13_00-00/CRM_data.csv

def get_hash(input_str, algorithm, salt=""):
    hasher = hashlib.new(algorithm)
    hasher.update((salt + input_str).encode('utf-8'))
    return hasher.hexdigest()

def main(input_path, output_path, col_to_hash, algorithm, truncate_length, salt):
    df = pd.read_csv(input_path, encoding='unicode_escape')

    # Need to remove Byte Order Marker at beginning of first column name
    for column in df.columns: 
        new_column_name = re.sub(r"[^0-9a-zA-Z.,-/_ ]", "", column)
        df.rename(columns={column: new_column_name}, inplace=True)

    if col_to_hash not in df.columns:
        print(f"Column '{col_to_hash}' not found.")
        return

    # Full hash
    df[f"{col_to_hash}_hash_full"] = df[col_to_hash].apply(lambda x: get_hash(str(x), algorithm, salt))

    # Optional truncation
    if truncate_length:
        df[f"{col_to_hash}_hash_truncated"] = df[f"{col_to_hash}_hash_full"].apply(lambda x: x[:truncate_length])
        
    # Remove PII
    df.pop('Email') 
    df.pop('First Name') 
    df.pop('Last Name') 

    # Reorder cols
    df_reorder = df[['Email_hash_full', 'Record ID - Contact', 'v1 Profession', 'v1 specialty all', 'v1 latest contract end date', 'Funnel Stage ID', 'job_suggestion_interested_employment_types', 'v1 employment type', 'v1 top places to work', 'Postal Code']]

    # Rename cols
    df_reorder.rename(columns={'Email_hash_full': 'email_hash_full', 'Record ID - Contact': 'record_id', 'v1 Profession': 'profession', 'v1 specialty all': 'specialty', 'v1 latest contract end date': 'contract_end_date', 'Funnel Stage ID': 'funnel_stage_id', 'job_suggestion_interested_employment_types': 'employment_type_ids', 'v1 employment type': 'employment_types', 'v1 top places to work': 'top_places_to_work', 'Postal Code': 'postal_code'}, inplace=True)

    # Write to CSV
    df_reorder.to_csv(output_path, index=False, sep='|')

    # Check for hash clashes if truncation is used
    if truncate_length:
        grouped = df.groupby(f"{col_to_hash}_hash_truncated").size().reset_index(name='counts')
        clashes = grouped[grouped['counts'] > 1]
        num_clashes = len(clashes)

        if num_clashes > 0:
            clash_percentage = (num_clashes / len(df)) * 100
            print(f"Warning: {num_clashes} hash clashes found ({clash_percentage:.2f}%).")
            
            clash_df = df[df[f"{col_to_hash}_hash_truncated"].isin(clashes[f"{col_to_hash}_hash_truncated"])]
            clash_log_path = f"{output_path.split('.')[0]}_log_clash.csv"
            clash_df.to_csv(clash_log_path, columns=[col_to_hash, f"{col_to_hash}_hash_full", f"{col_to_hash}_hash_truncated"], index=False)
            print(f"Clashes saved to {clash_log_path}.")
        else:
            print("No hash clashes found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hash a specific column in a CSV file.")
    parser.add_argument("input_path", help="Path to the input CSV file.")
    parser.add_argument("output_path", help="Path to save the output CSV file.")
    parser.add_argument("col_to_hash", help="Name of the column to hash.")
    parser.add_argument("-a", "--algorithm", default="sha224", help="Hash algorithm to use. Default is 'sha224'.")
    parser.add_argument("-l", "--length", type=int, help="Length to truncate the hash. Optional.")
    parser.add_argument("-s", "--salt", default="", help="Optional salt for the hash.")
    args = parser.parse_args()

    main(args.input_path, args.output_path, args.col_to_hash, args.algorithm, args.length, args.salt)
