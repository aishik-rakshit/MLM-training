class CFG:
    url = "https://www.investopedia.com/financial-term-dictionary-4769738"
    train_dir = "data"
    tokenizer_dir = "tokenizer"
    model_name = "klue/roberta-small"
    merged_data_train = "merged_data_train.txt"
    merged_data_val = "merged_data_val.txt"
    tokenizer = "tokenizer.json"
    num_links = 27
    chunk_size = 128
    batch_size = 64
    len = 512
    vocab_size = 52000
    seed = 2022