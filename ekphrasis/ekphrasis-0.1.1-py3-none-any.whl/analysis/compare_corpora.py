import pandas as pd

english = []
twitter = []
tags = []

mode = "segmenter"

eng = {line.split("\t")[0]: line.split("\t")[1] for line in open(mode + "_" + 'english.txt', 'r')}
tw = {line.split("\t")[0]: line.split("\t")[1] for line in open(mode + "_" + 'twitter.txt', 'r')}
for k, v in eng.items():
    if eng[k] != tw[k]:
        english.append(eng[k].strip())
        twitter.append(tw[k].strip())
        tags.append(k.strip())

df = pd.DataFrame(
    {'tags': tags,
     'english': english,
     'twitter': twitter,
     })

with open(mode + "_" + 'diffs.txt', 'w') as file_out:
    file_out.write(df.to_string(columns=["tags", "english", "twitter"]))
