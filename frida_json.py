import json
import pprint

 pp = pprint.PrettyPrinter(indent=4)

count = 0
with open("1h_mimibazar.analysis.proc.json", encoding = 'utf8') as file:
    for analysis in map(json.loads, file):
        if count == 5:
            break
        pp.pprint(analysis)
        count +=1

id_list = []
value_list = []
result = {}
count = 0
with open("1h_mimibazar.analysis.proc.json", encoding = 'utf8') as file:
    str = ""
    start_pos = 0
    for f in file:
        str += f
        try:
            analysis = json.loads(str)
            keywords = []
            for i in analysis["keywords"]:
                keywords.append(i['value'])
            result[analysis["id"]] = keywords
            count += 1
            if count % 1000 == 0:
                print("Done {0}".format(count))
            str = ""
        except JSONDecodeError as e:
            continue
print("Hotovo")

f = open("out.json", "w", encoding="utf-8")
f.write(json.dumps(result, indent=4,ensure_ascii=False))
f.flush()

id_list = []
value_list = []
result2 = {}
count = 0
with open("1h_mimibazar.analysis.proc.json", encoding = 'utf8') as file:
    str = ""
    start_pos = 0
    for f in file:
        str += f
        try:
            analysis = json.loads(str)
            lemmas = []
            for i in analysis["leadLemmas"]:
                for ii in i:
                    lemmas.append(ii['val'])
            result2[analysis["id"]] = lemmas
            count += 1
            if count % 1000 == 0:
                print("Done {0}".format(count))
            str = ""
        except JSONDecodeError as e:
            continue
print("Hotovo")

with open('c:\\Temp\\out_lemmas.json', 'w', encoding='utf-8') as fp:
    json.dump(result2, fp, indent=4,ensure_ascii=False)