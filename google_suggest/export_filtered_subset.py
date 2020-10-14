from random import shuffle
from google_suggest_persian import query_patterns
from persiantools import digits
from googlesearch import search

exclude_set = [
    "موارد ذيل",
    "نمیدونم چرا",
]

exclude_starts_with = [
    "دانلود",
    "دانلود آهنگ"
]

accepted_websites = [
    "fa.wikipedia", "bbc", "kayhan.ir", "etelanews", "nabzema.com", "delgarm.com/scientific/", "danesh" # , "tebyan.net"
]


def has_answer_in_accepted_websites(query):
    my_results_list = []
    for i in search(query,  # The query you want to run
                    num=10,  # Number of results per page
                    start=0,  # First result to retrieve
                    stop=10,  # Last result to retrieve
                    pause=2.0,  # Lapse between HTTP requests
                    ):
        my_results_list.append(i)

    has_overlap = False
    accepted_url = None
    for result in my_results_list:
        if has_overlap:
            break
        for accepted in accepted_websites:
            if accepted in result:
                has_overlap = True
                # print(f" yes overlap: {accepted} <-> {result}")
                accepted_url = result
                break

    return has_overlap, accepted_url

with open('already_exported.txt') as alreadyExportedf:
    already_exported_questions = [x.replace("\n", "").strip() for x in alreadyExportedf.readlines()]

outfile = open("questions_persian_filtered.txt", "+w")
with open("questions_persian.txt") as f:
    all_lines = list(f.readlines())

    shuffle(all_lines)

    counter = 0

    for line in all_lines:

        overlap = [pattern for pattern in exclude_set if pattern in line]
        if len(overlap) > 0:
            continue

        starts_with_overlap = [pattern for pattern in exclude_starts_with if line.startswith(pattern)]
        if len(starts_with_overlap) > 0:
            continue

        if len(line.split(" ")) < 6:
            continue

        matching_patterns = [q for q in query_patterns if q in f" {line} "]
        if len(matching_patterns) == 0:
            continue

        line = line.replace("\n", "")

        line = digits.en_to_fa(line)

        if "؟" not in line:
            line = line + "؟"

        if line in already_exported_questions:
            print(f" * already exported: {line}")
            continue

        accepted, accepted_url = has_answer_in_accepted_websites(line)

        if not accepted:
            continue

        counter += 1

        print(counter)
        if counter >= 4000:
            break

        print(line + "\t" + accepted_url)
        outfile.write(line + "\t" + accepted_url + "\n")

