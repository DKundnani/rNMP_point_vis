#!/usr/bin/env python3
import argparse
import matplotlib
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = 'Arial'
#print(matplotlib.matplotlib_fname())
import pandas as pd
import glob
import re

parser = argparse.ArgumentParser()
parser.add_argument('file')
parser.add_argument('ymax')
parser.add_argument('end')
parser.add_argument('type')
parser.add_argument('colorlist')
parser.add_argument('legend')
parser.add_argument('sep')
parser.add_argument('publish')
args = parser.parse_args()
file=args.file #file='gene_TSS_cpgoverlap_noXY*TSS.tab'
files=sorted(glob.glob('*'+file))
out=''.join(re.split(r"\*",file)).split('.')[0]
ymax=int(args.ymax)
end=args.end
type=args.type
color=args.colorlist #color="#ff7f0e,#d62728,#9467bd,#e377c2,#2ca02c"
colors=color.split(",")

if ymax > 3 and args.sep=='separate':
    y_gap=2
else:
    y_gap=1

if ymax > 20:
    y_gap=5

if ymax > 80:
    y_gap=20


#Read tab file
#Figure with only axis borders
fig = plt.figure(figsize=(2,2))
ax = fig.add_subplot(111)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_linewidth(0.75)
ax.tick_params('both', length=3, width=0.75)


for i in range(0,len(files)):
    #df= pd.read_csv(glob.glob(files[i])[0], sep='\t', header=None)
    df= pd.read_csv(files[i], sep='\t', header=None)
    df=df.fillna('')
    #Get end of file
    N=df.iloc[0,2:].tolist().index(end)
    mat=df.iloc[2:,2:(N+3)].astype(float)
    #Getting bins 
    bins=df.iloc[1,2:(N+3)].tolist()
    bins=[int(float(x)) for x in bins] 
    n=int(float(len(df.iloc[2:,0].tolist())/2))
    if args.sep=='separate':
        ax.plot(bins,(mat.iloc[:n]*2).mean(axis=0).tolist(), color=colors[i],linewidth=0.75)
        if mat.iloc[n][2]<0:
            ax.plot(bins,(mat.iloc[n:]*2).mean(axis=0).tolist(), color=colors[i],linewidth=0.75)
        else:
            ax.plot(bins,(mat.iloc[n:]*-2).mean(axis=0).tolist(), color=colors[i],linewidth=0.75)
    else:
        ax.plot(bins,mat.iloc[:len(df.iloc[2:,0])].mean(axis=0).tolist(), color=colors[i],linewidth=0.75)

if args.sep=='separate':
    ax.axhline(0, linestyle='-',color="black", linewidth=0.37)
    ax.axhline(-1, linestyle='--',color="black", linewidth=0.3)
    plt.yticks(ticks=[*range(-ymax,ymax+1,y_gap)],labels=list(map(abs,[*range(-ymax,ymax+1,y_gap)])),fontsize=12)
else:
    plt.yticks(ticks=[*range(0,ymax+1,y_gap)],labels=list(map(abs,[*range(0,ymax+1,y_gap)])),fontsize=12)

if ymax<=10:
    ax.axhline(1, linestyle='--',color="black", linewidth=0.3)
ax.axvline(29, linestyle='--',color="black", linewidth=0.3)

plt.xticks(ticks=[0,9,19,29,39,49,59],labels=['-3','-2','-1',type,'1','2','3'],fontsize=12)

if args.publish=='publish':
    # xticks color white
    plt.xticks(color='w')
    ax.set_xticklabels([])
    # yticks color white
    plt.yticks(color='w')
    ax.set_yticklabels([])

plt.savefig(f"{out}_all.png",dpi=1000,bbox_inches='tight')
