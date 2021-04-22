import sys
import re
import json


def decode_keyword(infile):
    word_list = []
    kw = {}
    with open(infile) as fin:
        for line in fin:
            fields = line.rstrip('\r\n').split("\t")
            intent = fields[0].strip()
            if fields[1].strip() == "keywords":
                continue
            # keywords = json.loads(fields[1].strip())
            keywords = fields[1].split("+")
            kw_type = False
            if kw_type == "整句匹配":
                kw_type = True
            else:
                kw_type = False
            for k in keywords:
                if k not in word_list:
                    word_list.append(k)
            kw.setdefault(intent, [])
            kw[intent].append((keywords, kw_type))
    return kw, word_list


def filter_all_file(word_list, infile, outfile):
    pattern = "|".join(word_list)
    with open(infile) as fin, open(outfile, 'w') as fout:
        for line in fin:
            fields = line.rstrip('\r\n').split("\t")
            query = fields[1].strip()
            match = re.search(pattern, query)
            if match:
                fout.write(line)


def output_kw(kw, infile, outfile, is_sort=True):
    intent_count = {}
    with open(infile) as fin, open(outfile, 'w') as fout:
        for line in fin:
            intents = []
            kws = []
            fields = line.rstrip('\r\n').split("\t")
            query = fields[1].strip()
            for k, v in kw.items():
                for s in v:
                    idx = 0
                    ll = len(s[0])
                    if s[1]:
                        if "".join(s[0]) == query:
                            if k not in intents:
                                intents.append(k)
                                intent_count.setdefault(k, 0)
                                intent_count[k] += 1
                            kws.append(json.dumps(s[0], ensure_ascii=False))
                    else:
                        # print(s, s[0], s[1])
                        if is_sort:
                            p = ".*?".join(s[0])
                            m = re.search(p, query)
                            if m:
                                idx = ll
                        else:
                            for ss in s[0]:
                                if ss in query:
                                    idx += 1
                    if idx == ll:
                        if k not in intents:
                            intents.append(k)
                            intent_count.setdefault(k, 0)
                            intent_count[k] += 1
                        kws.append(json.dumps(s[0], ensure_ascii=False))
            if intents:
                output = fields + [";".join(intents)] + [";".join(kws)]
                fout.write('\t'.join(output) + '\n')
    sort_v = dict(sorted(intent_count.items(),
                         key=lambda x: x[1], reverse=True))
    with open(outfile + ".count", 'w') as fout2:
        header = ["intent", "count"]
        fout2.write('\t'.join(header) + '\n')
        for k, v in sort_v.items():
            output = [k, f"{v}"]
            fout2.write('\t'.join(output) + '\n')


def uniq_query(infile, outfile):
    qc = {}
    with open(infile) as fin:
        for line in fin:
            fields = line.rstrip('\r\n').split("\t")
            query = fields[1].strip()
            qc.setdefault(query, 0)
            qc[query] += 1
    query_list = []
    with open(infile) as fin, open(outfile, 'w') as fout:
        for line in fin:
            fields = line.rstrip('\r\n').split("\t")
            query = fields[1].strip()
            if query not in query_list:
                count = qc[query]
                output = fields + [f"{count}"]
                fout.write('\t'.join(output) + '\n')
                query_list.append(query)


def split_kws(infile, outfile):
    with open(infile) as fin, open(outfile, 'w') as fout:
        for line in fin:
            fields = line.rstrip('\r\n').split("\t")
            kws = fields[-2].split(";")
            for kw in kws:
                output = fields[:-2] + [kw, fields[-1]]
                fout.write('\t'.join(output) + '\n')


if __name__ == "__main__":
    keyword_file = sys.argv[1]
    raw_file = sys.argv[2]
    outfile1 = f"{raw_file}.f1"
    outfile2 = f"{raw_file}.f2"
    outfile3 = f"{raw_file}.f3"
    outfile4 = f"{raw_file}.f4"
    kw, word_list = decode_keyword(keyword_file)
    # print(kw)
    filter_all_file(word_list, raw_file, outfile1)
    is_sort = False
    output_kw(kw, outfile1, outfile2, is_sort)
    uniq_query(outfile2, outfile3)
    split_kws(outfile3, outfile4)
