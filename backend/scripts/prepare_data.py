"""
Data preparation script for fine-tuning
Converts CSV dataset to JSONL format
"""

import pandas as pd
import json
from pathlib import Path
from typing import Optional
import argparse

def prepare_fine_tuning_data(
    csv_path: str,
    output_dir: str,
    train_size: float = 0.95,
    sample_size: Optional[int] = None,
    max_length: int = 512
):
    # Prepare data for fine-tuning
    print(f"Loading data from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    print(f"Original dataset size: {len(df)}")
    
    # Clean data
    df = df.dropna(subset=['text'])
    df = df[df['text'].str.strip() != '']
    df['text'] = df['text'].str[:max_length]
    
    print(f"After cleaning: {len(df)}")
    
    # Sample if needed
    if sample_size and sample_size < len(df):
        df = df.sample(n=sample_size, random_state=42)
        print(f"Sampled to: {len(df)}")
    
    # Shuffle
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Split
    split_idx = int(len(df) * train_size)
    train_df = df[:split_idx]
    val_df = df[split_idx:]
    
    print(f"Train: {len(train_df)}, Validation: {len(val_df)}")
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Save as JSONL
    train_file = output_path / "train_stories.jsonl"
    val_file = output_path / "val_stories.jsonl"
    
    print(f"\nSaving train data to {train_file}...")
    with open(train_file, 'w', encoding='utf-8') as f:
        for _, row in train_df.iterrows():
            json_obj = {"text": row['text']}
            f.write(json.dumps(json_obj, ensure_ascii=False) + '\n')
    
    print(f"Saving validation data to {val_file}...")
    with open(val_file, 'w', encoding='utf-8') as f:
        for _, row in val_df.iterrows():
            json_obj = {"text": row['text']}
            f.write(json.dumps(json_obj, ensure_ascii=False) + '\n')
    
    print("\nData preparation complete!")
    print(f"Train file: {train_file} ({len(train_df)} samples)")
    print(f"Val file: {val_file} ({len(val_df)} samples)")
    
    # Show sample
    print("\nSample story:")
    print(train_df['text'].iloc[0][:200] + "...")

def main():
    parser = argparse.ArgumentParser(description='Prepare data for fine-tuning')
    parser.add_argument('--csv', type=str, required=True, help='Path to CSV file')
    parser.add_argument('--output', type=str, default='./data/fine_tune_data', help='Output directory')
    parser.add_argument('--train-size', type=float, default=0.95, help='Train/val split ratio')
    parser.add_argument('--sample-size', type=int, default=None, help='Number of samples (optional)')
    parser.add_argument('--max-length', type=int, default=512, help='Max text length')
    
    args = parser.parse_args()
    
    prepare_fine_tuning_data(
        csv_path=args.csv,
        output_dir=args.output,
        train_size=args.train_size,
        sample_size=args.sample_size,
        max_length=args.max_length
    )

if __name__ == "__main__":
    main()