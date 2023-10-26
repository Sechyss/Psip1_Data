# Import necessary libraries
import math  # Import the math library for mathematical operations
import pandas as pd  # Import pandas library for data manipulation and analysis
import scipy.cluster.hierarchy as shc  # Import the hierarchy module from scipy.cluster for hierarchical clustering
import seaborn as sns  # Import seaborn library for data visualization
from matplotlib import pyplot as plt  # Import pyplot from matplotlib for creating plots
from matplotlib.patches import Patch  # Import Patch from matplotlib.patches for creating legend patches

# Read input data from files
blastp_output = pd.read_table('/Users/u2176312/OneDrive - University of Warwick/'
                              'Thesis/Paper Draft/Distance_PMEs_Psip1_PhoAaty_corrected.tsv', header=None)
Df_Ap = pd.read_excel('/Users/u2176312/OneDrive - University of Warwick/'
                      'Thesis/Paper Draft/Dict_ID_AlkPh.xlsx', sheet_name='Sheet1')

# Extract 'ID' and 'AlkP' columns and convert them to lists
ids = list(str(x) for x in Df_Ap['ID'].values)

# Create a dictionary from 'ID' and 'AlkP' columns
Dict_AP = pd.Series(Df_Ap['AlkP'].values, index=ids).to_dict()

# Define column names for the blastp_output DataFrame
columns = ['Taxa1', 'Taxa2', '% identity', 'length', 'mismatches', 'gap open', 'q. start', 'q.end', 's. start',
           's. end', 'evalue', 'bitscore']

# Rename columns of the blastp_output DataFrame
blastp_output.columns = columns

# Extract the first part of 'Taxa1' and 'Taxa2' columns, split by underscores
blastp_output['Taxa1'] = blastp_output['Taxa1'].apply(lambda x: str(x).split('_')[0])
blastp_output['Taxa2'] = blastp_output['Taxa2'].apply(lambda x: str(x).split('_')[0])

# Create an empty DataFrame with unique 'Taxa1' values as both index and columns
collector_df = pd.DataFrame(index=list(set(blastp_output['Taxa1'])), columns=list(set(blastp_output['Taxa1'])))

# Fill collector_df with logarithmically transformed evalue values
for index, row in blastp_output.iterrows():
    collector_df[blastp_output.loc[index]['Taxa1']][blastp_output.loc[index]['Taxa2']] = \
        math.log(1 + float(blastp_output.loc[index]['evalue']))

# Fill NaN values in collector_df with 3
collector_df = collector_df.fillna(3)

# Define a dictionary mapping AlkPhos names to colors
lut = {
    'Psip1': '#FF6A6A',
    'PhoX_Flavo': '#8968CD',
    'PhoX': '#8B3A62',
    'PhoA': '#6E8B3D',
    'PhoD': '#008B8B',
    'PafA': '#FFB90F',
    'PhoAaty': '#083D77'
}

# Map AlkPhos names to colors using the lut dictionary and the Dict_AP Series
phosphatases = pd.Series(Dict_AP).map(lut)

# Perform hierarchical clustering on collector_df using the Ward method
dend_reordered = shc.linkage(collector_df, method='ward', optimal_ordering=True)

# Create a figure for the clustering dendrogram
fig = plt.figure(figsize=(22, 18))

# Create a clustermap using seaborn
clustering_dend = sns.clustermap(collector_df, metric="euclidean", method="ward",
                                 row_colors=phosphatases,
                                 col_colors=phosphatases,
                                 row_linkage=dend_reordered, col_linkage=dend_reordered,
                                 cmap="YlGnBu")

# To display all x-axis labels
xticks = list(range(0, len(clustering_dend.data2d.columns)))
clustering_dend.ax_heatmap.set_xticks(xticks)
clustering_dend.ax_heatmap.set_xticklabels(clustering_dend.data2d.columns, fontsize=6)

# To display all y-axis labels
yticks = list(range(0, len(clustering_dend.data2d.index)))
clustering_dend.ax_heatmap.set_yticks(yticks)
clustering_dend.ax_heatmap.set_yticklabels(clustering_dend.data2d.index, fontsize=6)

# Create legend patches for AlkPhos names and their corresponding colors
handles = [Patch(facecolor=lut[name]) for name in lut]

# Add a legend to the plot
plt.legend(handles, lut, title='AlkPhos',
           bbox_to_anchor=(1, 1), bbox_transform=plt.gcf().transFigure, loc='upper right')

# Uncomment the following line to save the plot as a PDF file
plt.savefig('/Users/u2176312/OneDrive - University of Warwick/'
            'Thesis/Paper Draft/Clustergram_blastp_ALL_PMES.pdf', dpi=600)

# Display the plot
plt.show()
