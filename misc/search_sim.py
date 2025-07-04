import os, sys
import re
import collections
import pickle
import gzip
from prompt_toolkit import PromptSession
from prompt_toolkit.application import get_app
from prompt_toolkit import print_formatted_text

from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.shortcuts import ProgressBar

from nltk.stem.snowball import SnowballStemmer
snoball_stemmer = SnowballStemmer('english')

import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="コマンドラインオプションのサンプル")
    parser.add_argument('--max', type=int, default=40, help='maximal search results')
    parser.add_argument('--col', type=int, default=80, help='size of column')
    parser.add_argument('--db', type=str, default='db.pkl', help='database')
    parser.add_argument('inputfiles', nargs='*', help='inputfiles')
    return parser.parse_args()

def extract_text_from_latex(text):
    text = text + "\n"
    text = re.sub(r'[^\x00-\x7F]', '', text)
    text = re.sub(r'%.*?\n', '\n', text)
    text = re.sub(r"(''|``)", '"', text)
    text = re.sub(r'\\(begin|end)\{(book|abstract|quote)\}', '\n', text)
    text = re.sub(r'\\(textit|textbf)\s*\{(.*?)\}', r' \2 ', text)
    text = re.sub(r'\\(ref|cite)\{(.*?)\}', r' [NUM] ', text)
    for env in "equation", "eqnarray", "align", "gather", "math":
        ptn = r"\\begin\{ENV\}.*?\\end\{ENV\}".replace("ENV", env)
        text = re.sub(ptn, ' [MATH] ', text, flags=re.DOTALL)
    for env in "figure", "table", "quote", "tikzpicture":
        ptn = r"\\begin\{ENV\}.*?\\end\{ENV\}".replace("ENV", env)
        text = re.sub(ptn, ' ', text, flags=re.DOTALL)
    # インライン数式環境
    for l, r in [("$$","$$"),("$","$"),(r"\[", r"\]"),(r"\(", r"\)")]:
        ptn = re.escape(l) + r"([-\+\w\s\.]+)" + re.escape(r)
        text = re.sub(ptn, ' \1 ', text, flags=re.DOTALL)
        ptn = re.escape(l) + r".*?" + re.escape(r)
        text = re.sub(ptn, ' [MATH] ', text, flags=re.DOTALL)
    # LaTeXコマンドを除去 (引数あり・なし両方対応)
    text = re.sub(r'\\\w+\*?(\[[^\]]*\])?(\{[^\}]*\})?', ' ', text)
    # 不要な波括弧を除去
    text = re.sub(r'[{}~]', ' ', text)
    # 余計な空白や改行を整理
    text = re.sub(r'\s+(,|\.|:|;)', r'\1', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text


def create_db(filelist):
    book = []
    index = collections.defaultdict(set)

    with ProgressBar() as pb:
        for n in pb(range(len(filelist))):
            item = filelist[n]
            if item.endswith(".gz"):
                fh = gzip.open(item, "rt")
            else:
                fh = open(item, "rt")
            text = fh.read()
            fh.close
            book += extract_text_from_latex(text).split()
    with ProgressBar() as pb:
        for i, item in enumerate(pb(book)):
            # item = book[i]
            stem = snoball_stemmer.stem(item)
            if stem:
                index[stem].add(i)
    return book, index

def search(kw):
    cur = {}
    flag_first = True
    for i, item in enumerate(kw.split()):
        stem = snoball_stemmer.stem(item)
        if item == "*":
            continue
        if stem in index:
            if flag_first:
                cur = {x+i for x in index[stem]}
                flag_first = False
                continue
            else:
                cur = {x for x in cur if (x+i) in index[stem]}
        else:
            cur.clear()
            break
    return cur

args = parse_args()
print (args.inputfiles)


file_db = "db.pkl"

if os.path.isfile("db.pkl"):
    with open(file_db, "rb") as fh:
        db = pickle.load(fh)
else:
    file_list = []
    for item in sys.argv[1:]:
        if os.path.isfile(item):
            if item.endswith(".tex") or item.endswith(".tex.gz"):
                file_list += [item]
    db = create_db(file_list)
    with open(file_db, "wb") as fh:
        pickle.dump(db, fh)

book, index = db

session = PromptSession()


while True:
    kw = session.prompt(">>> ")

    data = []

    if kw.endswith("?"):
        item = kw.split()[-1][:-1]
        tmp = set([])
        for stem in index:
            if stem.startswith(item):
                tmp.add(stem)
        tmp2 = set([])
        for stem in list(tmp)[:100]:
            for i in list(index[stem])[:100]:
                tmp2.add(book[i].lower())
        print(" ".join(list(tmp2)[:100]))
        continue
    
    cur = search(kw)
    

    if cur:
        for i in cur:
            pre = " ".join(book[i-10:i])
            match = " ".join(book[i:i+len(kw.split())])
            post = " ".join(book[i+len(kw.split()):i+len(kw.split())+10])
            data += [(match, post, pre)]
        data.sort()

        n = total_width = get_app().output.get_size().columns
        l = get_app().output.get_size().rows
        m = int(n/2)
        for i, (match, post, pre) in enumerate(data[:l]):
                print_formatted_text(
                    FormattedText([
                        ('', pre[-m:] + " "),
                        ('bold', match[:n-m]),
                        ('', " " + post[:n-m])
                    ]))
                    
                    

