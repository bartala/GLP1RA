# -*- coding: utf-8 -*-

import pandas as pd
import os
import matplotlib.pyplot as plt

PTH = '/.../data'

edges = pd.read_csv(os.path.join(PTH,'g_edgelist.csv')) # no pubmed
edges.columns = ['node_from', 'node_to','weight']
edges

nodes = pd.concat(
              [
                  edges[['node_from','weight']].rename(columns={'node_from': 'node'}),
                  edges[['node_to','weight']].rename(columns={'node_to': 'node'})
              ],
              axis = 0
).reset_index(drop=True)


nodes = nodes.groupby('node')['weight'].sum().reset_index()

nodes

nodes['weight'].sum()

"""# Define side effect frequency

The frequency of a drug side effect in the population can be:

* very rare (<1 in 10,000),
* rare (1 in 10,000 to 1 in 1000),
* infrequent (1 in 1000 to 1 in 100),
* frequent (1 in 100 to 1 in 10), or
* very frequent (>1 in 10)
"""

!pip install wordcloud matplotlib

nodes['freq'] = nodes['weight']/nodes['weight'].max()

nodes.loc[ (nodes['freq'] < 0.0001),'group'] = 'very rare'
nodes.loc[ (nodes['freq'] >= 0.0001) & (nodes['freq'] < 0.001) ,'group'] = 'rare'
nodes.loc[ (nodes['freq'] >= 0.001) & (nodes['freq'] < 0.01) ,'group'] = 'infrequent'
nodes.loc[ (nodes['freq'] >= 0.01) & (nodes['freq'] < 0.1) ,'group'] = 'frequent'
nodes.loc[ (nodes['freq'] >= 0.1),'group'] = 'very frequent'

nodes['group'].value_counts()

import seaborn as sns
import matplotlib.pyplot as plt

# Assuming you have a DataFrame 'nodes' with a 'group' column
word_counts = nodes['group'].value_counts().reindex(["very rare", "rare", "infrequent", "frequent", "very frequent"])

sns.barplot(x=word_counts.index, y=word_counts.values, color='lightblue')

# Add labels and a title
plt.xlabel('Side effect frequency class value')
plt.ylabel('Counts')
plt.title('Side Effect Counts')

# Add numbers on top of each bar
for i, count in enumerate(word_counts.values):
    label = str(count) if count > 0 else "0"
    plt.text(i, count, label, ha='center', va='center', fontsize=11)

# Save the figure as a PDF
plt.savefig("barplot_side_effect_frequency_class.pdf", format="pdf")

# Show the plot
plt.show()

nodes['group'].value_counts()

import matplotlib.pyplot as plt
import numpy as np

# Sort the DataFrame by "Number of Drugs" in descending order
df = nodes.sort_values(by='freq', ascending=False)

# Define the order in which groups should be plotted
group_order = ['very frequent', 'frequent', 'infrequent', 'rare', 'very rare']  # Customize this order

# Define a colormap for "group" values
colormap = plt.get_cmap('tab10')  # You can choose a different colormap


# Create the line plot with color mapping
plt.figure(figsize=(10, 5))  # Adjust the figure size as needed
for group in group_order:
    group_df = df[df['group'] == group]
    if not group_df.empty:  # Check if the group has members
        color = colormap(group_order.index(group) % 10)  # Ensure it loops through colors if there are more than 10 groups
        plt.plot(group_df['node'], group_df['freq'], marker='o', linestyle='-', label=f'{group}', color=color)

# Rotate the x-axis labels for better readability
plt.xticks(rotation=90, ha='right')

# Add labels and title
plt.xlabel('Side Effect')
plt.ylabel('Fraction of Side Effect')
plt.title('Long-Tailed Distribution of Side Effects')

# Add a legend to distinguish groups for the groups with data
plt.legend()

# Adjust the layout to prevent truncation of x-axis labels
plt.tight_layout()

# Save the figure as a PDF
plt.savefig("side_effect_distribution.pdf", format="pdf")

# Show the plot
plt.show()






import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patheffects as pe
from matplotlib import gridspec

# --- 1. CONFIGURATION ---
filename = "Figure_C_Risk_Stratification.pdf"
dpi = 300 

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Helvetica', 'Arial', 'DejaVu Sans']

# The "Nano Banana" Effect (White outline for text/lines)
stroke_white = [pe.withStroke(linewidth=2.5, foreground='white')]

# --- 2. DATA ---
age_groups = ['18-24', '25-34', '35-44', '45-54', '55-64', '65+']
x = np.arange(len(age_groups))
user_counts = [2246, 5582, 5035, 3491, 1989, 1117]

data_high = {
    'GI / Motility': {
        'y': [10.4, 11.1, 12.0, 12.2, 14.2, 14.9], 
        'color': '#C0392B', 'marker': 'o', 'rho': '1.00', 'p': '<0.001', 'side': 'right', 'text_y': 15.1
    }
}

data_low = {
    'Insomnia': {
        'y': [0.8, 1.7, 2.0, 3.5, 4.5, 6.4], 
        'color': '#E67E22', 'marker': 's', 'rho': '0.94', 'p': '0.005', 'side': 'right', 'text_y': 6.8
    },
    'Skin Aging': {
        'y': [0.7, 1.2, 1.8, 2.9, 4.0, 4.5], 
        'color': '#F1C40F', 'marker': '^', 'rho': '0.94', 'p': '0.005', 'side': 'right', 'text_y': 5.0
    },
    'Taste Changes': {
        'y': [0.5, 1.2, 2.0, 3.0, 4.0, 4.2], 
        'color': '#D35400', 'marker': 'D', 'rho': 0.89, 'p': '0.019', 'side': 'right', 'text_y': 3.7
    },
    'Dehydration': {
        'y': [0.2, 0.15, 0.15, 0.2, 0.3, 2.8], 
        'color': '#8E44AD', 'marker': 'P', 'rho': '0.83', 'p': '0.042', 'side': 'right', 'text_y': 2.4
    },
    'Weight Changes': {
        'y': [2.5, 2.7, 2.1, 1.9, 0.6, 0.1], 
        'color': '#2980B9', 'marker': 'v', 'rho': '-0.94', 'p': '0.005', 'side': 'left', 'text_y': 3.4
    },
    'Hormonal/Repro': {
        'y': [2.0, 2.3, 1.8, 1.7, 0.9, 0.7], 
        'color': '#27AE60', 'marker': 'X', 'rho': '-0.94', 'p': '0.005', 'side': 'left', 'text_y': 1.6
    },
    'Neurological': {
        'y': [0.7, 0.7, 0.5, 0.1, 0.4, 0.4], 
        'color': '#34495E', 'marker': '*', 'rho': '-0.89', 'p': '0.019', 'side': 'left', 'text_y': 0.2
    }
}

# --- 3. LAYOUT ---
fig = plt.figure(figsize=(12, 7))
# Ratio: Top (1.2), Mid (4.0), Bot (1.5)
ratios = [1.2, 4.0, 1.5]
gs = gridspec.GridSpec(3, 1, height_ratios=ratios, hspace=0.05)

ax_top = plt.subplot(gs[0])
ax_mid = plt.subplot(gs[1])
ax_bot = plt.subplot(gs[2])

# --- 4. PLOTTING FUNCTION ---
def plot_lines_polished(ax, dataset):
    for name, d in dataset.items():
        ax.plot(x, d['y'], marker=d['marker'], color=d['color'], 
                 linewidth=2.5, markersize=8, zorder=3, path_effects=stroke_white)
        
        label_text = f"{name}\n($\\rho$={d['rho']}, $p$={d['p']})"
        
        if d['side'] == 'right':
            ax.annotate(label_text, xy=(x[-1], d['y'][-1]), xytext=(x[-1] + 0.2, d['text_y']),
                         color=d['color'], fontsize=9, fontweight='bold', va='center',
                         path_effects=stroke_white,
                         arrowprops=dict(arrowstyle="-", color=d['color'], lw=1.5, shrinkB=5))
        else:
            ax.annotate(label_text, xy=(x[0], d['y'][0]), xytext=(x[0] - 0.2, d['text_y']),
                         color=d['color'], fontsize=9, fontweight='bold', va='center', ha='right',
                         path_effects=stroke_white,
                         arrowprops=dict(arrowstyle="-", color=d['color'], lw=1.5, shrinkB=5))

plot_lines_polished(ax_top, data_high)
plot_lines_polished(ax_mid, data_low)

# --- 5. BROKEN AXIS ---
ax_top.set_ylim(10, 16.5) 
ax_mid.set_ylim(-0.5, 7.5)

ax_top.spines['bottom'].set_visible(False)
ax_mid.spines['top'].set_visible(False)
ax_top.xaxis.tick_top()
ax_top.tick_params(labeltop=False)
ax_mid.xaxis.tick_bottom()
ax_mid.set_xticklabels([])

# Parallel Slope Correction
d = 0.015 
ratio_correction = ratios[0] / ratios[1] 
d_tall = d * ratio_correction 

# Draw Slopes
kwargs = dict(transform=ax_top.transAxes, color='k', clip_on=False, linewidth=1.5)
ax_top.plot((-d, +d), (-d, +d), **kwargs)        
ax_top.plot((1 - d, 1 + d), (-d, +d), **kwargs)  

kwargs.update(transform=ax_mid.transAxes) 
ax_mid.plot((-d, +d), (1 - d_tall, 1 + d_tall), **kwargs)  
ax_mid.plot((1 - d, 1 + d), (1 - d_tall, 1 + d_tall), **kwargs)  

# Grid & Labels
for ax in [ax_top, ax_mid]:
    ax.grid(True, linestyle=':', alpha=0.5, zorder=0)
    ax.set_xlim(-1.5, 6.5)
    ax.tick_params(axis='y', labelsize=10)

ax_mid.set_ylabel('Reporting Rate (%)', fontsize=12, fontweight='bold', labelpad=10)
ax_mid.yaxis.set_label_coords(-0.07, 0.6) 

# --- 6. BAR CHART FOOTER ---
bars = ax_bot.bar(x, user_counts, color='#95A5A6', edgecolor='white', linewidth=1.5, width=0.6, zorder=3)
for bar in bars:
    height = bar.get_height()
    ax_bot.text(bar.get_x() + bar.get_width()/2., height + 400,
                 f'N={int(height):,}', ha='center', va='bottom', 
                 fontsize=9, fontweight='bold', color='#555555', path_effects=stroke_white)

ax_bot.set_ylabel('Users', fontsize=11, fontweight='bold')
ax_bot.set_xticks(x)
ax_bot.set_xticklabels(age_groups, fontsize=11, fontweight='bold')

# --- ADDED X-LABEL HERE ---
ax_bot.set_xlabel('Age Group (Years)', fontsize=12, fontweight='bold', labelpad=10)

ax_bot.set_ylim(0, 9500)
ax_bot.grid(False)
ax_bot.spines['top'].set_visible(False)
ax_bot.set_xlim(-1.5, 6.5)

# --- 7. SAVE ---
plt.savefig(filename, format='pdf', bbox_inches='tight', dpi=dpi)
print(f"Success! Figure saved as: {filename}")
plt.show()
