# MLM-training
MLM training with custom tokeizer

Demo Notebook: https://colab.research.google.com/drive/10ZGJ05O9Ty70qsiPX16UKHFV33SB9zle?usp=sharing

Metric used is Perplexity

Postprocessing function should be avoided except replacing short formas as most models are trained on common crawl data.
Tokenizer is a custom finetuned roberta base tokenizer on the financial data provided.
Model is a roberta-base model.
