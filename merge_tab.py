#!/usr/bin/env python3

import argparse
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#python3 $TAVIR/Deeptools_sep_ind_cellline_TSS_TTS.py $out/${base}_${group}_cen.tab 30 3.0Kb cntr D62728 nolegend notsep

parser = argparse.ArgumentParser()
parser.add_argument('pos')
parser.add_argument('neg')
parser.add_argument('end')
parser.add_argument('out')
parser.add_argument('negative')

args = parser.parse_args()
pos=args.pos
neg=args.neg
end=args.end
#Read tab file
df1= pd.read_csv(pos, sep='\t', header=None)
df2= pd.read_csv(neg, sep='\t', header=None)

df1=df1.fillna('')
df2=df2.fillna('')

#Get end of file
N=df1.iloc[0,2:].tolist().index(end)
mat1=df1.iloc[2:,2:(N+3)].astype(float)
mat2=df2.iloc[2:,2:(N+3)].astype(float)

#Reverse the mat and merge
mat2.columns=np.flip(mat2.columns)
if args.negative=='negative':
    mat2=mat2*-1

mat=(mat1+mat2)/4

#Insert mat back into OG dataframe
df1.iloc[2:,2:(N+3)]=mat

#Write the matrix in tab format
df1.to_csv(args.out,sep='\t', header=False,index=False)