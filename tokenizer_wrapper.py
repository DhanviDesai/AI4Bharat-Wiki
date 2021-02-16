from hindi_tokenizer import AnuvaadHindiTokenizer
from eng_tokenizer import AnuvaadEngTokenizer
import os
from pathlib import Path

b_path = 'Scraped_Files'
hi_tokenizer = AnuvaadHindiTokenizer()
eng_tokenizer = AnuvaadEngTokenizer()
path = 'Tokenized_Files'
Path(path).mkdir(parents=True,exist_ok=True)
for f in os.listdir(b_path):
    if '-hi' in f:
        with open(os.path.join(b_path,f),'r',encoding="utf-16") as g:
            text = hi_tokenizer.tokenize(g.read())
    if '-en' in f:
        with open(os.path.join(b_path,f),'r',encoding="utf-16") as g:
            text = eng_tokenizer.tokenize(g.read())
    with open(os.path.join(path,f),'a+',encoding='utf-16') as g:
        for line in text:
            g.write(line+'\n')