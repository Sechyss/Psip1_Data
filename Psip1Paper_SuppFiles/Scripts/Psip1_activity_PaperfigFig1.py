import os
import statistics

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib as mpl

from scipy import optimize

from Cyanopackage.ActivityAnalysisClass import MetalActivityData, michaelis_menten, transform_substratedf_productdf

mpl.rcParams['font.size'] = 25
mpl.rcParams['font.family'] = 'Arial'
fig, ax = plt.subplots(2, 2, figsize=(22, 18), dpi=450)
# %% Metal figure

os.chdir('/Users/u2176312/OneDrive - University of Warwick/Thesis/Paper Draft/')
TableMetals = pd.read_excel('/Users/u2176312/OneDrive - University of Warwick/Thesis/Paper '
                            'Draft/Andrew_PsipMetals.xlsx', sheet_name='Sheet3', header=0, index_col=0)
x_value = list(TableMetals.index)
ax[0, 0].spines['top'].set_visible(False)
ax[0, 0].spines['right'].set_visible(False)

shapedict = {
    'Calcium': 's',
    'Iron': 'o',
    'Calcium + Iron': '*'
}
for column in TableMetals.columns:
    if '_std' in str(column):
        continue

    if 'Calcium +' in str(column):
        y = list(TableMetals[column])
        error = list(TableMetals[column + '_std'])
        ax[0, 0].errorbar(x_value, y, yerr=error, capsize=3, capthick=1,
                          fmt='--' + str(shapedict[str(column)]),
                          markerfacecolor='black',
                          color='black',
                          markeredgecolor='black',
                          label=str(column),
                          markersize=16)

    elif 'Calcium' in str(column):
        y = list(TableMetals[column])
        error = list(TableMetals[column + '_std'])
        ax[0, 0].errorbar(x_value, y, yerr=error, capsize=3, capthick=1,
                          fmt='--' + str(shapedict[str(column)]),
                          markerfacecolor='black',
                          color='black',
                          markeredgecolor='black',
                          label=str(column),
                          markersize=12)

    else:
        y = list(TableMetals[column])
        error = list(TableMetals[column + '_std'])
        ax[0, 0].errorbar(x_value, y, yerr=error, capsize=3, capthick=1,
                          fmt='-' + str(shapedict[str(column)]),
                          markerfacecolor='none',
                          color='black',
                          markeredgecolor='black',
                          label=str(column),
                          markersize=14)
ax[0, 0].set_xlabel('Time (mins)')
ax[0, 0].set_ylabel('Abs(405nm)')
ax[0, 0].set_title('A', loc='left', weight='bold', y=1.1, fontsize=28)
ax[0, 0].legend(loc='upper left', fontsize=20)

# %% Bis-pNPP figure

Diester = pd.read_excel('/Users/u2176312/OneDrive - University of Warwick/Thesis/Paper '
                        'Draft/Diesterase_test.xlsx', sheet_name='Sheet2', header=0)

x_values = [x for x in Diester.columns if '_std' not in x]
error_columns = [x for x in Diester.columns if '_std' in x]
means = Diester[x_values].values.tolist()
means = [item for sublist in means for item in sublist]
means[1] = 0  # because the value of bispnpp is negative is changed to 0
error = Diester[error_columns].values.tolist()
error = [item for sublist in error for item in sublist]

x_values = [x.replace('F. johnsoniae', '$\it{F. johnsoniae}$') for x in x_values]
x_values = [x.replace('PNPP', '$\it{p}$NPP') for x in x_values]
ax[0, 1].bar(x_values, means, yerr=error, align='center', ecolor='black', capsize=10, edgecolor='black', color='white')
ax[0, 1].set_ylabel('Abs (405nm)')
ax[0, 1].set_xticks(x_values)
ax[0, 1].tick_params(axis='x', rotation=20)
ax[0, 1].spines['top'].set_visible(False)
ax[0, 1].spines['right'].set_visible(False)
ax[0, 1].set_xticklabels(x_values)
ax[0, 1].set_title('B', loc='left', weight='bold', y=1.1, fontsize=28)
ax[0, 1].yaxis.grid(False)

ax[0, 1].set_ylim([0, 1.3])

# %% pH figure
os.chdir('/Users/u2176312/Downloads')

trial = pd.read_excel('Psip1_experiment_pag53_table.xlsx', sheet_name='Study_noOut', index_col=0)
experiment = MetalActivityData(trial)
curves, rvalue = experiment.fit_curve()

pH = list([list(curves['pH6.8'].values()), list(curves['pH7.5'].values()), list(curves['pH8.8'].values()),
           list(curves['pH9.4'].values()), list(curves['pH9.8'].values()), list(curves['pH10.4'].values()),
           list(curves['pH11.2'].values())])

r_score = list([list(rvalue['pH6.8'].values()), list(rvalue['pH7.5'].values()), list(rvalue['pH8.8'].values()),
                list(rvalue['pH9.4'].values()), list(rvalue['pH9.8'].values()), list(rvalue['pH10.4'].values()),
                list(rvalue['pH11.2'].values())])
means = [statistics.mean(x) for x in pH]
error = [statistics.stdev(x) for x in pH]
x = [6.8, 7.5, 8.8, 9.4, 9.8, 10.4, 11.2]

ax[1, 0].errorbar(x, means, yerr=error, fmt='-o', capsize=3, capthick=1, color='black', markersize=10)
ax[1, 0].set_xlabel('pH values')
ax[1, 0].set_ylabel(r'$\Delta$Abs(405nm) min$^{-1}$ mg protein$^{-1}$')
ax[1, 0].spines['top'].set_visible(False)
ax[1, 0].spines['right'].set_visible(False)
ax[1, 0].spines['bottom'].set_color('black')
ax[1, 0].spines['left'].set_color('black')
ax[1, 0].set_title('C', loc='left', weight='bold', y=1.1, fontsize=28)

# %% Michaelis-Menten figure

# --- Loading of dataframes with data normalized by the negative control
concentrations_1 = pd.read_excel('Psip1_experiment_pag61_table.xlsx', sheet_name='Test', index_col=0)
concentrations_2 = pd.read_excel('Psip1_experiment_pag63_2_table.xlsx', sheet_name='Test', index_col=0)
AdditionalCon = pd.read_excel('Psip1_experiment_pag61_table.xlsx', sheet_name='Test2', index_col=0)

# --- Loading of standard curve tables
standard_1 = pd.read_excel('Psip1_experiment_pag61_table.xlsx', sheet_name='StandardCurve', index_col=0)
standard_2 = pd.read_excel('Psip1_experiment_pag63_2_table.xlsx', sheet_name='StandardCurve', index_col=0)
standard_3 = pd.read_excel('Psip1_experiment_pag61_table.xlsx', sheet_name='StandardCurveTest', index_col=0)

# --- Transformation of df to productdf to fit the curves of Michaelis-Menten
product_df1 = transform_substratedf_productdf(concentrations_1, standard_1, 0.0020)
product_df2 = transform_substratedf_productdf(concentrations_2, standard_2, 0.0020)
AddtionalProductdf = transform_substratedf_productdf(AdditionalCon, standard_3, 0.0028)

Concat_df = pd.merge(product_df1, AddtionalProductdf, left_index=True, right_index=True)

# --- Specify the concentrations used for the assays
amounts_1 = [0, 2, 2.5, 3, 3.5, 4, 5, 10, 15]
amounts_2 = [0, 1.5, 1.8, 2.2, 2.4, 2.5, 3, 4, 5, 6, 10]

# --- Fitting of the curves and combination of data into one single df
experiment = MetalActivityData(Concat_df)
curves, rvalue_fit = experiment.fit_curve()

velocity = [list(curves[str(x)].values()) for x in amounts_1]

means = [statistics.mean(x) for x in velocity]
error = [statistics.stdev(x) for x in velocity]

experiment_2 = MetalActivityData(product_df2)
curves_2, rvalue_fit_2 = experiment_2.fit_curve()

velocity_2 = np.array([list(curves_2[str(x)].values()) for x in amounts_2])
means_2 = [statistics.mean(x) for x in velocity_2]
error_2 = [statistics.stdev(x) for x in velocity_2]

# --- Combination of the points for Michaelis-Menten
for d in curves_2.keys():
    if d not in curves.keys():
        curves.update({d: curves_2[d]})
    else:
        for i in curves[d]:
            curves[d][i] = [curves[d][i], curves_2[d][i]]

x_pos = [0, 1.5, 1.8, 2, 2.2, 2.4, 2.5, 3, 3.5, 4, 5, 6, 10, 15]

velocityMM = []

for i in x_pos:
    collector = []
    for element in curves[str(i)].values():
        if type(element) == list:
            collector.append(element[0]);
            collector.append(element[1])
        else:
            collector.append(element)
    velocityMM.append(collector)

meansMM = [statistics.mean(x) for x in velocityMM]
errorMM = [statistics.stdev(x) for x in velocityMM]

# --- Fitting of the
p0 = [10, 10]
params, cv = optimize.curve_fit(michaelis_menten, amounts_1, means)
vmax, km = params
print("Vmax = ", vmax)
print("Km = ", km)
print('Estimated variance (Vm, Km) = ' + str(cv[0, 0]) + ', ' + str(cv[1, 1]))
print('Estimated standard devitation (Vm, Km) = ', np.sqrt(np.diag(cv)))

residuals = means - michaelis_menten(amounts_1, *params)
ss_res = np.sum(residuals ** 2)
ss_tot = np.sum((means - np.mean(means)) ** 2)
r_squared = 1 - (ss_res / ss_tot)

ax[1, 1].errorbar(amounts_1, means, yerr=error, fmt='o', capsize=3, capthick=1, color='black', markersize=10)
ax[1, 1].errorbar(amounts_2, means_2, yerr=error_2, fmt='ko', capsize=3, capthick=1, markerfacecolor='none',
                  markeredgecolor='black', markersize=10)
ax[1, 1].plot(np.linspace(0, 15, 1000), michaelis_menten(np.linspace(0, 15, 1000), vmax, km),
              "k--", label='Fitted Michaelis-Menten equation')
ax[1, 1].text(5, 1, u"R\u00b2= {:0.2f}".format(r_squared), style='italic', fontsize=22)
ax[1, 1].spines['top'].set_visible(False)
ax[1, 1].spines['right'].set_visible(False)
ax[1, 1].spines['bottom'].set_color('black')
ax[1, 1].spines['left'].set_color('black')
ax[1, 1].set_xlabel('$\it{p}$NPP (μM)')
ax[1, 1].set_ylabel(r'Velocity (nmoles min$^{-1}$ mg protein$^{-1}$)')
ax[1, 1].set_title('D', loc='left', weight='bold', y=1.1, fontsize=28)

ax[1, 1].legend(loc='lower right', fontsize=22)


plt.tight_layout()
plt.savefig('Fig1_paper.pdf', dpi=1000)
