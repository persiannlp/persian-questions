import json
import random
import requests
import numpy as np
import time
import spacy
from tqdm import tqdm


def query_and_return(prefix):
    time.sleep(0.3)
    r = requests.get(f"http://google.com/complete/search?client=chrome&q={prefix}")
    if r.status_code == 200:
        # save it
        content = r.content.decode("utf-8", errors='replace')
        content = json.loads(content)
        return content[1]
    else:
        return []


query_patterns = [
    " چه کسی ",
    " کی ",
    " مال چه کسی",
    " چرا ",
    " کدام ",
    " کجا ",
    " چه زمانی ",
    " چرا ",
    " چگونه ",
    " باید ",
    " شاید ",
    " نباید ",
    " می توان ",
    " نمی توان ",
    " خواهد ",
    " نخواهد ",
    " نمی توانند ",
    " می کند ",
    " می کنند ",
    " دارد ",
    " داشت ",
    " هستم ",
    " هستند ",
    " هست ",
    " نباید ",
    " نیست ",
    " می باید ",
    " می بایست ",
    " چه ",
    " چیست "
    " کیست "
]


persian_alphabet = ['آ', 'ا', 'ب', 'پ', 'ت', 'ث', 'ج', 'چ', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'ژ', 'س', 'ش', 'ص', 'ض',
                    'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ک', 'گ', 'ل', 'م', 'ن', 'و', 'ه', 'ی']

def crawl_questions_continue():

    # then, augment the results
    all_results = []
    with open("questions_persian.txt") as f:
        for l in f.readlines():
            all_results.append(l.replace("\n", ""))

    past_queries = []
    for idx in tqdm(range(0, 40)):
        random.shuffle(all_results)
        for result in all_results[:1000]:
            idx_cut = 7 + idx*2

            # find the index of the next space
            try:
                idx_cut = result.index(" ", idx_cut)
            except:
                print(f" ** skipping `{result}` because no space was found after index {idx_cut} . . .")
                continue

            if len(result) < idx_cut - 1:
                print(" ** skipping because it's too short")
                continue

            prefix = result[:idx_cut + 1]

            # if prefix not in query_patterns:
            #     continue
            matching_patterns = [q for q in query_patterns if q in f" {prefix} "]
            if len(matching_patterns) == 0:
                print(f">>>> skipping: {l}")
                continue
            else:
                print(f"matching_patterns: {matching_patterns}")

            if prefix in past_queries:
                continue
            else:
                past_queries.append(prefix)

            for character in persian_alphabet:
                prefix1 = prefix + character
                print(f" ** {prefix1}")
                output = query_and_return(prefix1)
                # all_results.extend(output)
                for out in output:
                    if len(out) < 15:
                        print(f" ----> {out}: X")
                        continue
                    if out not in all_results:
                        all_results.append(out)
                        print(f" ----> {out}: Y")
                    else:
                        print(f" ----> {out}: X2")
                print(len(all_results))
                # print(all_results[-1])
            all_results = list(set(all_results))
            all_results = sorted(all_results)
            f = open("questions_persian.txt", "w")
            f.write("\n".join(all_results))
            f.close()



if __name__ == "__main__":
    crawl_questions_continue()
