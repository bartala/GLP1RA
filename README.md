# GLP1 Project

## Overview
Early identification of emerging risks from fragmented, noisy evidence remains a central
challenge in the Intelligence Phase of decision making, where weak signals must be
interpreted under deep uncertainty. We introduce ALERT (Advanced Learning for Early Risk Tracking), a multimodal AI-enabled
decision support framework that operationalizes organizational sense-making through
evidence triangulation and intelligence augmentation. ALERT integrates social media
discourse, biomedical literature, and structured pharmacovigilance data to detect,
calibrate, and prioritize candidate adverse side effects (ASEs). Applied to the domain of GLP-1 receptor agonists, ALERT empirically identified 134 ASEs and surfaces 21 novel signals absent from manufacturer labels and established databases. ALERT uncovers a stable logarithmic relationship between social media frequency and validated sources ($R^2= 0.99$), enabling principled credibility calibration of weak signals. A graph convolutional network captures ASE co-occurrence structure to prioritize risks (F1 = 0.81). Beyond detection, ALERT supports actionable decision support via age-stratified risk profiling ($p < 0.05$) and prediction of treatment discontinuation drivers (F1 = 0.78). Notably, several candidate ASEs initially identified only in social media, including aura-related migraine, ketonemia, and psychiatric effects, were later reported in post-2024 clinical and observational studies, supporting ALERT’s early signal detection capability. This work demonstrates how AI transforms unstructured data into auditable decision cues in uncertain medical and business settings.

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
