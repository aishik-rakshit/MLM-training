from torch.utils.data import Dataset
from transformers import LineByLineTextDataset, AutoTokenizer, AutoModelForMaskedLM, AutoConfig, DataCollatorForLanguageModeling, TrainingArguments, Trainer
from config import CFG
from glob import glob
from pathlib import Path
import warnings
import math
from tokenizers.implementations import ByteLevelBPETokenizer
from tokenizers.processors import BertProcessing
from preprocess import preprocess

def concatenate_files(filenames, outfile):
    with open(outfile, 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(preprocess(line))

if __name__ == "__main__":

    config = AutoConfig.from_pretrained(CFG.model_name)
    model = AutoModelForMaskedLM.from_config(config = config)

    tokenizer = AutoTokenizer.from_pretrained(CFG.tokenizer_dir)

    src_files = [file for file in glob(f"{CFG.train_dir}/*.txt")]

    
    train_src_files = src_files[:int(0.8*len(src_files))]
    val_src_files = src_files[int(0.8*len(src_files)):]

    concatenate_files(train_src_files, CFG.merged_data_train)
    concatenate_files(val_src_files, CFG.merged_data_val)

    train_dataset = LineByLineTextDataset(
        tokenizer = tokenizer,
        file_path = CFG.merged_data_train ,
        block_size = 128  # maximum sequence length
    )

    val_dataset = LineByLineTextDataset(
        tokenizer = tokenizer,
        file_path = CFG.merged_data_val ,
        block_size = 128  # maximum sequence length
    )

    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm_probability=0.15)

    logging_steps = len(train_dataset) // CFG.batch_size

    training_args = TrainingArguments(
        output_dir=f"{CFG.model_name.split('/')[-1]}-yali",
        overwrite_output_dir=True,
        evaluation_strategy="epoch",
        learning_rate=2e-5,
        weight_decay=0.01,
        per_device_train_batch_size=CFG.batch_size,
        per_device_eval_batch_size=CFG.batch_size,
        fp16=False,
        logging_steps=logging_steps,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        data_collator=data_collator,
    )

    eval_results = trainer.evaluate()
    print(f">>> Initial Perplexity: {math.exp(eval_results['eval_loss']):.2f}")

    trainer.train()

    eval_results = trainer.evaluate()
    print(f">>> Final Perplexity: {math.exp(eval_results['eval_loss']):.2f}")



