import re

ptn = re.compile("(\S+)\s+configuration=\s*(\d+)")

with open("XDATCAR", "r") as fh:
      icount = 0
      header = ""
      for line in fh:
            tmp = ptn.search(line)
            if tmp:
                  mode = tmp.group(1)
                  icount = int(tmp.group(2))
                  fh_out = open(f"xdat{icount:03d}.CONTCAR.vasp", "w")
                  print(fh_out.name)
                  fh_out.write(f"{header}{mode}\n")
            else:
                  if icount > 0:
                        fh_out.write(line)
                  else:
                        header += line
                        
