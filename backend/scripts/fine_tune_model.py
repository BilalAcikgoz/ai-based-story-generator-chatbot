# Fine-tuning script for local training

import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    BitsAndBytesConfig
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from datasets import load_dataset
import argparse
from pathlib import Path

def fine_tune_model(
    model_name: str = "gpt2",
    train_file: str = "./data/fine_tune_data/train_stories.jsonl",
    val_file: str = "./data/fine_tune_data/val_stories.jsonl",
    output_dir: str = "./models/fine_tuned",
    use_qlora: bool = True,
    num_epochs: int = 1,
    batch_size: int = 4,
    learning_rate: float = 2e-4
):
    # Fine-tune model with QLoRA
    if not torch.cuda.is_available():
        print("WARNING: No GPU detected. Fine-tuning will be very slow!")
        print("Consider using Kaggle or Google Colab instead.")
        return
    
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    
    # Load tokenizer
    print(f"Loading tokenizer: {model_name}")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token
    
    # Load datasets
    print(f"Loading datasets...")
    dataset = load_dataset('json', data_files={
        'train': train_file,
        'validation': val_file
    })
    
    print(f"Train: {len(dataset['train'])}, Val: {len(dataset['validation'])}")
    
    # Tokenization
    def tokenize_function(examples):
        result = tokenizer(
            examples["text"],
            truncation=True,
            max_length=512,
            padding="max_length",
        )
        result["labels"] = result["input_ids"].copy()
        return result
    
    print("Tokenizing...")
    tokenized_dataset = dataset.map(
        tokenize_function,
        batched=True,
        remove_columns=["text"]
    )
    
    # Model config
    if use_qlora:
        print("Using QLoRA (4-bit quantization)")
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
        )
        
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            quantization_config=bnb_config,
            device_map={"": 0},
            torch_dtype=torch.float16,
        )
        model = prepare_model_for_kbit_training(model)
        model.gradient_checkpointing_enable()
        
        # LoRA config
        lora_config = LoraConfig(
            r=8,
            lora_alpha=16,
            target_modules=["c_attn"],
            lora_dropout=0.05,
            bias="none",
            task_type="CAUSAL_LM"
        )
        model = get_peft_model(model, lora_config)
        
    else:
        print("Using full fine-tuning")
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16
        )
    
    model.print_trainable_parameters()
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=num_epochs,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        gradient_accumulation_steps=4,
        learning_rate=learning_rate,
        warmup_steps=100,
        weight_decay=0.01,
        max_grad_norm=0.3,
        eval_strategy="epoch",
        save_strategy="epoch",
        fp16=True,
        gradient_checkpointing=True,
        logging_steps=50,
        report_to="none",
    )
    
    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset["train"],
        eval_dataset=tokenized_dataset["validation"],
    )
    
    # Train
    print("\nStarting training...")
    trainer.train()
    
    # Save
    print(f"\nSaving model to {output_dir}")
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    
    # Evaluate
    print("\nEvaluating...")
    metrics = trainer.evaluate()
    print(f"Eval loss: {metrics['eval_loss']:.4f}")
    print(f"Perplexity: {torch.exp(torch.tensor(metrics['eval_loss'])):.2f}")
    
    print("\nFine-tuning complete!")

def main():
    parser = argparse.ArgumentParser(description='Fine-tune model')
    parser.add_argument('--model', type=str, default='gpt2', help='Base model')
    parser.add_argument('--train', type=str, default='./data/fine_tune_data/train_stories.jsonl')
    parser.add_argument('--val', type=str, default='./data/fine_tune_data/val_stories.jsonl')
    parser.add_argument('--output', type=str, default='./models/fine_tuned')
    parser.add_argument('--epochs', type=int, default=1)
    parser.add_argument('--batch-size', type=int, default=4)
    parser.add_argument('--lr', type=float, default=2e-4)
    parser.add_argument('--no-qlora', action='store_true', help='Disable QLoRA')
    
    args = parser.parse_args()
    
    fine_tune_model(
        model_name=args.model,
        train_file=args.train,
        val_file=args.val,
        output_dir=args.output,
        use_qlora=not args.no_qlora,
        num_epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.lr
    )

if __name__ == "__main__":
    main()