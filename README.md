# GLP1 Project

## Overview
Unreported adverse side effects (ASEs) of prescription medications pose significant risks and are difficult to identify post-release. 
Guided by the Design Science Research paradigm, we present ALERT (Advanced Learning for Early Risk Tracking), an AI-powered analytical information system for early risk detection across complex domains. 
ALERT integrates heterogeneous data from social media posts, ChatGPT-generated insights, pharmaceutical reports, and biomedical knowledge, utilizing graph learning and natural language processing to transform fragmented data into actionable insights. 
We applied ALERT to the popular glucagon-like peptide-1 receptor agonists (GLP-1 RAs) medications for treating diabetes and obesity, a rapidly growing market estimated at \$133.5 billion by 2030.
ALERT identified 21 potential ASEs overlooked by clinical trials. 
Prioritization of these ASEs was based on temporal trends and predicted frequency, achieving strong performance (F1-score 0.81, AUC 0.83). 
ALERT provides an early warning system to detect risks, prioritize interventions, and support proactive clinical decision-making and risk mitigation.

# Repository Contents
## Papaer LateX Documents

`/LaTex/sn-article.tex` - main manuscript.

`/LaTex/sb-bibluigraphy.bib` - refecences of the manuscript.

## Running the Code

`.env.example` - variable and credentials needed to run the code.

`ASE_ASE_Network.R` - code for building the ASE-ASE network.

`GNN` - train a CGN model to classify edges in the ASE-ASE network as frequent or not.

`Reddit` - collect and analyze Reddit data.

`X.py` - collect and analyze X (formerly Twitter) data.

`pubmed` - collect and analyze PubMed data.

`sentiment_analysis` - analyze sentiment in Reddit and X.

`plots.py` - create plots of long-tailed ASE distribution and barplot of ASE frequency category


`plots.R` - clusters of the main component of the ASE-ASE graph.

`requirements.txt` - required python packages to run the code.

## Miscellaneous
Please send any questions you might have about the code and/or the algorithm to...



## Citing our work
If you find this code useful for your research, please consider citing us:
```
@article{GLP1RA,
  title     = {Leveraging AI for ALERT: Advanced Learning for Early Risk Tracking},
  author    = {},
  journal   = {},
  volume    = {},
  number    = {},
  pages     = {from page– to page},
  year      = {}
}
