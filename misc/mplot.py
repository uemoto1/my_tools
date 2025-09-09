import argparse
from pylab import *

parser = argparse.ArgumentParser()
parser.add_argument("eqlist", nargs="+")
parser.add_argument("-x", "--xlim", default="0,1", type=str, help="Range of x")
parser.add_argument("-y", "--ylim", default="0,1", type=str, help="Range of y")
parser.add_argument("-c", "--color", default="k", type=str, help="color")
parser.add_argument("-w", "--width", default=2.0, type=float, help="width")
parser.add_argument("-n", "--nsample", default=100, type=int, help="sampling")
args = parser.parse_args()

xmin, xmax = [float(r) for r in args.xlim.split(",")]
ymin, ymax = [float(r) for r in args.ylim.split(",")]
xr = abs(xmax - xmin)
yr = abs(ymax - ymin)
r = max([xr, yr])

figure(figsize=[xr/r*5, yr/r*5])
axes().set_aspect(1.0)
xlim(xmin, xmax)
ylim(ymin, ymax)

xlabel("")
ylabel("")
xticks([])
yticks([])

gca().spines['right'].set_visible(False)
gca().spines['top'].set_visible(False)
gca().spines['bottom'].set_visible(False)
gca().spines['left'].set_visible(False)
tight_layout()

from numpy import *
for eq in args.eqlist:
    x = linspace(xmin, xmax, args.nsample)
    y = linspace(ymin, ymax, args.nsample)
    if eq.startswith("x="):
        x = eval(eq[2:])
    elif eq.startswith("y="):
        y = eval(eq[2:])
    else:
        print(f"ERROR! {eq}")
        continue
    plot(x, y, color=args.color, linewidth=args.width)

show()
