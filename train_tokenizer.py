from operator import imod
from config import CFG
import glob
import os
from transformers import AutoTokenizer
from preprocess import preprocess
from tokenizers import  ByteLevelBPETokenizer

def get_corpus(filenames):
    for fname in filenames:
        with open(fname) as infile:
            for line in infile:
                yield preprocess(line)

if __name__ == "__main__":

    paths = glob.glob(f"{CFG.train_dir}/*.txt")
    text_corpus = get_corpus(paths)
    tokenizer = AutoTokenizer.from_pretrained(CFG.model_name)

    # Customize training
    tokenizer.train_new_from_iterator(text_corpus, vocab_size=52000)

    # Save files to disk
    os.makedirs(CFG.tokenizer_dir, exist_ok=True)
    tokenizer.save_pretrained(CFG.tokenizer_dir)