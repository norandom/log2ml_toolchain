#!/usr/bin/env python3

import sys
import argparse
import subprocess
import pandas as pd
from pathlib import Path
import zipfile


def check_kaggle_credentials():
    """Check for Kaggle credentials file"""
    kaggle_dir = Path.home() / '.kaggle'
    kaggle_json = kaggle_dir / 'kaggle.json'
    if kaggle_json.exists():
        # Ensure proper permissions
        kaggle_json.chmod(0o600)
        return True
    print("Error: Kaggle credentials not found at ~/.kaggle/kaggle.json")
    print("\nTo set up Kaggle credentials:")
    print("1. Create a Kaggle account at https://www.kaggle.com")
    print("2. Go to https://www.kaggle.com/account")
    print("3. Click 'Create New API Token' to download kaggle.json")
    print("4. Create directory: mkdir -p ~/.kaggle")
    print("5. Move the downloaded file: mv kaggle.json ~/.kaggle/")
    print("6. Set permissions: chmod 600 ~/.kaggle/kaggle.json")
    sys.exit(1)


def download_dataset():
    """Download the dataset from Kaggle"""
    dataset = "mariusciepluch/log2ml-blindtest-maldoc-activity-capture"
    filename = "lab_logs_blindtest_activity_sysmon_1000samples_july_28_2024_filtered_clean.csv"
    zip_filename = filename + ".zip"
    # Create data directory if it doesn't exist
    data_dir = Path('data')
    data_dir.mkdir(exist_ok=True)
    # Download using kaggle API
    try:
        print(f"Downloading dataset from {dataset}...")
        subprocess.run(
            ['kaggle', 'datasets', 'download', '-d', dataset, '-f', filename, '--unzip'],
            check=True
        )
        # Move the file to data directory
        src_file = Path(filename)
        dst_file = data_dir / filename
        # Check if we have a zip file
        zip_file = Path(zip_filename)
        if zip_file.exists():
            print("Extracting zip file...")
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(data_dir)
            zip_file.unlink()  # Remove zip file
            print(f"Extracted to {dst_file}")
        elif src_file.exists():
            src_file.rename(dst_file)
            print(f"Moved file to {dst_file}")
        if dst_file.exists():
            # Read and display dataset info
            df = pd.read_csv(dst_file)
            print("\nDataset Information:")
            print(f"Number of samples: {len(df)}")
            print("\nColumns:")
            for col in df.columns:
                print(f"- {col}")
            print(f"\nSample text:\n{df['text'].iloc[0]}")
        else:
            raise FileNotFoundError(f"Could not find dataset file at {dst_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error downloading dataset: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def main():
    """Main function to handle command line arguments and download the dataset."""
    parser = argparse.ArgumentParser(description='Download Log2ML dataset from Kaggle')
    parser.parse_args()
    check_kaggle_credentials()
    download_dataset()


if __name__ == '__main__':
    main()
