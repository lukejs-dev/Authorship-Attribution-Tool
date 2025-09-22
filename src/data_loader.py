# src/data_loader.py
import os
import pandas as pd

def load_and_group_discord_data(channels_directory):
    """
    Loads data from multiple CSV files, groups message content, and counts messages by AuthorID.
    Returns a tuple of (grouped_content_dict, message_counts_dict).
    """
    all_messages_df = pd.DataFrame()
    try:
        csv_files = [os.path.join(channels_directory, f) for f in os.listdir(channels_directory) if f.endswith('.csv')]
    except FileNotFoundError:
        print(f"Error: Directory not found at {channels_directory}")
        return {}, {}

    if not csv_files:
        print(f"No CSV files found in directory: {channels_directory}")
        return {}, {}

    print(f"Found {len(csv_files)} CSV files to process.")

    for file in csv_files:
        try:
            df = pd.read_csv(file, encoding='utf-8', low_memory=False)
        except UnicodeDecodeError:
            try:
                df = pd.read_csv(file, encoding='latin1', low_memory=False)
            except Exception as e:
                print(f"Warning: Could not read {file}. Skipping. Error: {e}")
                continue
        except Exception as e:
            print(f"Error reading {file}: {e}. Skipping.")
            continue

        if 'AuthorID' in df.columns and 'Content' in df.columns:
            df = df[['AuthorID', 'Content']].dropna(subset=['AuthorID', 'Content'])
            all_messages_df = pd.concat([all_messages_df, df], ignore_index=True)
        else:
            print(f"Warning: Skipping {file} due to missing 'AuthorID' or 'Content' columns.")

    if all_messages_df.empty:
        return {}, {}

    grouped_messages = all_messages_df.groupby('AuthorID')['Content'].apply(lambda x: ' '.join(x.astype(str))).to_dict()
    message_counts = all_messages_df.groupby('AuthorID').size().to_dict()

    return grouped_messages, message_counts

def load_and_combine_target_documents(individual_directory):
    """
    Loads and combines the content of all text files in the target directory.
    """
    combined_content = ""
    try:
        txt_files = [os.path.join(individual_directory, f) for f in os.listdir(individual_directory) if f.endswith('.txt')]
    except FileNotFoundError:
        print(f"Error: Directory not found at {individual_directory}")
        return None

    if not txt_files:
        print(f"No text files found in directory: {individual_directory}")
        return None

    print(f"Found {len(txt_files)} target text file(s).")

    for file_path in txt_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                combined_content += f.read() + "\n"
        except Exception as e:
            print(f"Error reading {file_path}: {e}. Skipping.")
            continue

    return combined_content if combined_content.strip() else None