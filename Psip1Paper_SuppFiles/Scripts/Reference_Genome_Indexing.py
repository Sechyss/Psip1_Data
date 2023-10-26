#  import of packages needed for further analysis
import os

import pandas as pd
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

#  Setting of working directory and, files and upload of data into panda dataframe
os.chdir(
    '/Users/u1866168/Documents/OneDrive - University of Warwick/MHC_Scripts/Cyanobacteria/Python_results/')
header = ["index_genome", "Cluster", "Product", "NTSEQ", "AASEQ", "Genus", "Strain"]
Table_clusters = pd.read_csv(
    '/Users/u1866168/Documents/OneDrive - University of Warwick/MHC_Scripts/Cyanobacteria/Python_results/GeneKeyTable.csv',
    names=header)
f1 = open("Reference_Genome.fna", "w")
f2 = open("Reference_Genome.txt", "w")
f1.close()
f2.close()

#  Analysis of all sequences in database, creation of the fasta file for reference genome and index_genome for bbsplit
for index, row in Table_clusters.iterrows():
    f1 = open("Reference_Genome.fna", "a")
    f2 = open("Reference_Genome.txt", "a")
    NTSeq = Seq(row['NTSEQ'].replace(" ", ""))
    ID = str(row['index_genome'])
    FastaNT = SeqRecord(NTSeq[:len(NTSeq) - 2], id=ID, description="")
    # f1 = open(row["index_genome"]+".fna", "w")
    SeqIO.write(FastaNT, f1, "fasta")
    Length = str(len(FastaNT.seq))
    f2.write(str(row['index_genome']) + "    " + Length + '\n')
    f1.close()
    f2.close()
