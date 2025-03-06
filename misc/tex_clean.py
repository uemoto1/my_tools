import sys

level = 0
flag_empty = False
for line in sys.stdin:
    tmp = line.strip()
    if not tmp:
        if flag_empty:
            continue
        else:
            sys.stdout.write("\n")
            flag_empty = True
    else:
        if tmp.startswith("%"):
            continue
        if r"\%" not in tmp:
            tmp = tmp.split("%")[0].strip()
        flag_empty = False
        level -= tmp.count(r"\end")
        nf = tmp.count("{") - tmp.count("}")
        if nf < 0:
            level += nf
        sys.stdout.write((" " * (4*level)) + " ".join(tmp.split()) + "\n")
        if nf > 0:
            level += nf
        level +=  tmp.count(r"\begin")
