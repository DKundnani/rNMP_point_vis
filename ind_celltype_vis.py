#!/usr/bin/env python3

import argparse
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = 'Arial'
#print(matplotlib.matplotlib_fname())
import pandas as pd
#python3 $TAVIR/Deeptools_sep_ind_cellline_TSS_TTS.py $out/${base}_${group}_cen.tab 30 3.0Kb cntr D62728 nolegend notsep

parser = argparse.ArgumentParser()
parser.add_argument('file')
parser.add_argument('ymax')
parser.add_argument('end')
parser.add_argument('type')
parser.add_argument('color')
parser.add_argument('legend')
parser.add_argument('sep')
parser.add_argument('publish')

args = parser.parse_args()
file=args.file


ymax=int(args.ymax)
type=args.type
end=args.end
color=args.color
#Read tab file
df= pd.read_csv(file, sep='\t', header=None)
df=df.fillna('')
#Get end of file
N=df.iloc[0,2:].tolist().index(end)
mat=df.iloc[2:,2:(N+3)].astype(float)
#Getting x-axis labels
x_lab=df.iloc[0,2:(N+3)].tolist()
xx_lab=list(filter(None, x_lab))
xx_lab
#Getting bins 
bins=df.iloc[1,2:(N+3)].tolist()
bins=[int(float(x)) for x in bins] 
#Getting sample names
lab=df.iloc[2:,0].tolist()
if "_" in lab[0]:
    lab=[i.split('_')[1] for i in lab]
    N=int(len(lab)/2)
else:
    N=int(len(lab))


#Defining colours for max amount of samples
cols=["#1f77b4","#ff7f0e","#2ca02c","#d62728","#9467bd","#8c564b"]
if ymax > 3 and args.sep=='separate':
    y_gap=2
else:
    y_gap=1

if ymax > 20:
    y_gap=5

if ymax > 80:
    y_gap=20

if ymax > 5 and args.sep=='overlap':
    y_gap=2

#Figure with only axis borders
#fig = plt.figure(figsize=(3,3))
#ax = fig.add_subplot(111)
#ax.spines['right'].set_visible(False)
#ax.spines['top'].set_visible(False)

#Plotting lines based on number of samples
#for i in range(N):
#    ax.plot(bins,mat.iloc[i].tolist(), label=lab[i], color=cols[i],linewidth=1)
#    ax.plot(bins,mat.iloc[i+N].tolist(),color=cols[i], linewidth=1)

#ax.axhline(1, linestyle='--',color="black", linewidth=0.3)
#ax.axhline(-1, linestyle='--',color="black", linewidth=0.3)
#plt.xticks(ticks=[0,9,19,29,39,49,59],labels=['-3','-2','-1',type,'1','2','3'])
#plt.xticks(ticks=[x_lab.index(i) for i in xx_lab],labels=xx_lab)
#plt.yticks(ticks=[*range(-ymax,ymax+1,2)],labels=list(map(abs,[*range(-ymax,ymax+1,2)])))

#Legend - usually needed for one type regions (right most needed for the set of samples)
#if args.legend=='legend':
#    plt.legend(frameon=False,bbox_to_anchor=(1.10, 1.10), loc="upper right", prop={'size': 7})
#plt.savefig(f"{file}.png",dpi=1000,bbox_inches='tight')


#Avg with min and max
fig = plt.figure(figsize=(2,2))
ax = fig.add_subplot(111)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_linewidth(0.75)
ax.tick_params(width=0.75)

#ax.plot(bins,mat.iloc[:N].mean(axis=0).tolist(), color="#d62728",linewidth=1)
#ax.plot(bins,mat.iloc[N:].mean(axis=0).tolist(), color="#1f77b4",linewidth=1)
if args.sep=='separate':
    ax.plot(bins,(mat.iloc[:N]*2).mean(axis=0).tolist(), color='#'+color,linewidth=0.75)
    plt.fill_between(bins, (mat.iloc[:N]*2).mean(axis=0)-(mat.iloc[:N]*2).sem(axis=0), (mat.iloc[:N]*2).mean(axis=0)+(mat.iloc[:N]*2).sem(axis=0), color='#'+color, alpha=0.2,linewidth=0.75)
    if mat.iloc[N][2]<0:
        ax.plot(bins,(mat.iloc[N:]*2).mean(axis=0).tolist(), color='#'+color,linewidth=0.75)
        plt.fill_between(bins, (mat.iloc[N:]*2).mean(axis=0)-(mat.iloc[N:]*2).sem(axis=0), (mat.iloc[N:]*2).mean(axis=0)+(mat.iloc[N:]*2).sem(axis=0), color='#'+color, alpha=0.2,linewidth=0.75)
    else:
        ax.plot(bins,(mat.iloc[N:]*-2).mean(axis=0).tolist(), color='#'+color,linewidth=0.75)
        plt.fill_between(bins, (mat.iloc[N:]*-2).mean(axis=0)-(mat.iloc[N:]*-2).sem(axis=0), (mat.iloc[N:]*-2).mean(axis=0)+(mat.iloc[N:]*-2).sem(axis=0), color='#'+color, alpha=0.2,linewidth=0.75)
    ax.axhline(-1, linestyle='--',color="black", linewidth=0.3)
    plt.yticks(ticks=[*range(-ymax,ymax+1,y_gap)],labels=list(map(abs,[*range(-ymax,ymax+1,y_gap)])),fontsize=12)
    plt.ylim(-ymax, ymax)
elif args.sep=='overlap':
    ax.plot(bins,(mat.iloc[:N]*2).mean(axis=0).tolist(), color='#60C2B1',linewidth=0.75) #2166ac
    plt.fill_between(bins, (mat.iloc[:N]*2).mean(axis=0)-(mat.iloc[:N]*2).sem(axis=0), (mat.iloc[:N]*2).mean(axis=0)+(mat.iloc[:N]*2).sem(axis=0), color='#60C2B1', alpha=0.2,linewidth=0)
    if mat.iloc[N][2]<0:
        ax.plot(bins,(mat.iloc[N:]*2).mean(axis=0).tolist(), color='#A77AE6',linewidth=0.75) #b2182b
        plt.fill_between(bins, (mat.iloc[N:]*2).mean(axis=0)-(mat.iloc[N:]*2).sem(axis=0), (mat.iloc[N:]*2).mean(axis=0)+(mat.iloc[N:]*2).sem(axis=0), color='#A77AE6', alpha=0.2,linewidth=0)
    else:
        ax.plot(bins,(mat.iloc[N:]*2).mean(axis=0).tolist(), color='#A77AE6',linewidth=0.75) #b2182b
        plt.fill_between(bins, (mat.iloc[N:]*2).mean(axis=0)-(mat.iloc[N:]*2).sem(axis=0), (mat.iloc[N:]*2).mean(axis=0)+(mat.iloc[N:]*2).sem(axis=0), color='#A77AE6', alpha=0.2,linewidth=0)
    plt.yticks(ticks=[*range(0,ymax+1,y_gap)],labels=list(map(abs,[*range(0,ymax+1,y_gap)])),fontsize=12)
    plt.ylim(0, ymax)
else:
    ax.plot(bins,mat.iloc[:len(lab)].mean(axis=0).tolist(), color='#'+color,linewidth=0.75)
    plt.fill_between(bins, mat.iloc[:len(lab)].mean(axis=0)-mat.iloc[:len(lab)].sem(axis=0), mat.iloc[:len(lab)].mean(axis=0)+mat.iloc[:N].sem(axis=0), color='#'+color, alpha=0.2,linewidth=0)
    plt.yticks(ticks=[*range(0,ymax+1,y_gap)],labels=list(map(abs,[*range(0,ymax+1,y_gap)])),fontsize=12)

#plt.fill_between(bins, mat.iloc[:N].min(axis=0).tolist(), mat.iloc[:N].max(axis=0).tolist(), color='#'+color, alpha=0.2,linewidth=0.75)
#plt.fill_between(bins, mat.iloc[N:].min(axis=0).tolist(), mat.iloc[N:].max(axis=0).tolist(), color='#'+color, alpha=0.2,linewidth=0.75)
if ymax<=10:
    ax.axhline(1, linestyle='--',color="black", linewidth=0.3)
ax.axvline(29, linestyle='--',color="black", linewidth=0.3)
ax.axhline(0, linestyle='-',color="black", linewidth=0.37)
plt.xticks(ticks=[0,9,19,29,39,49,59],labels=['-3','-2','-1',type,'1','2','3'],fontsize=12)


if args.publish=='publish':
    # xticks color white
    plt.xticks(color='w')
    ax.set_xticklabels([])
    # yticks color white
    plt.yticks(color='w')
    ax.set_yticklabels([])

if args.sep=='separate':
    plt.savefig(f"{file}_ribbon_separate.svg",format='svg',bbox_inches='tight')
elif args.sep=='overlap':
    plt.savefig(f"{file}_ribbon_overlap.svg",format='svg',bbox_inches='tight')
else:
    plt.savefig(f"{file}_ribbon.svg",format='svg',bbox_inches='tight')