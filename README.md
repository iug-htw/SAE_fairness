<p align="center">
  <img src="assets/htw_logo.jpg" alt="HTW Berlin Logo" width="300"/>
</p>

# Probing Religion, Violence, and Geography in Large Language Models

**Mechanistic Interpretability with Sparse Autoencoders (SAEs)**
_(AEQUITAS Workshop @ ECAI 2025)_

---

## Project Overview

This repository supports our paper:

**"Mechanistic Interpretability with SAEs: Probing Religion, Violence, and Geography in Large Language Models"**
Presented at: <br/>
_AEQUITAS 2025: Workshop on Fairness and Bias in AI,_
<br/> _co-located with the 28th European Conference on Artificial Intelligence (ECAI 2025),_
<br/> _Bologna, Italy_.

### Contribution to Research

This project contributes to the growing field of **mechanistic interpretability** by applying
**Sparse Autoencoders (SAEs)** to probe how **Large Language Models (LLMs)** internally represent social concepts.

Instead of analyzing surface-level model outputs, we directly investigate the **latent conceptual structures**
encoded in SAEs. This provides a window into how associations between **religions, violence, and geography**
are encoded — even when they are not explicitly surfaced in model predictions.

---

## Motivation

The key research questions:

1. **RQ1 – Intra-group coherence:**
   Do prompts about the same religion consistently activate a shared conceptual core?

2. **RQ2 – Religion–violence associations:**
   Do religion-related prompts overlap with violence-related features?

3. **RQ3 – Geographic associations:**
   Do religion-related prompts activate geographic concepts (e.g., Christianity–Europe, Islam–Middle East)?

4. **RQ4 – Cross-model variation:**
   Are these associations stable across different LLM architectures and SAE configurations?

---

## Research Team

This project was conducted at **HTW Berlin (Hochschule für Technik und Wirtschaft Berlin)** by:

- **Prof. Dr. Katharina Simbeck** – Professor of Business Informatics (Information Management) - HTW Berlin
- **Mariam Mahran** – Research Assistant, AI & Interpretability - HTW Berlin

---

## Methodology

Our approach integrates **SAEs + Neuronpedia API**:

1. **Data Collection**

   - Religion/violence prompts are submitted to the **Neuronpedia API**.
   - Top-activating SAE features are retrieved, along with activation texts.

2. **Feature Analysis**

   - Extract logits and activation patterns.
   - Detect duplicate features across queries.

3. **Overlap Analysis**

   - Count shared features within a religion group (RQ1).
   - Count overlaps between religion and violence groups (RQ2).

4. **Semantic Probing**

   - Scan activation texts for **crime-related** and **geographic** keywords.
   - Aggregate mentions into interpretable tables and charts (RQ2, RQ3).

5. **Cross-Model Comparison**

   - Apply the pipeline across **Gemma, GPT2-small, LLaMA3.1-8B** and different SAE source sets.
   - Identify stable vs. model-specific associations (RQ4).

---

## Key Findings

- **Intra-Group Consistency (RQ1):** All five religions (Christianity, Islam, Judaism, Buddhism, Hinduism) showed comparable levels of internal cohesion.

- **Religion–Violence Associations (RQ2):** when comparing overlaps between religion-related prompts and violence-related prompts, **Islam consistently scored the highest Violence Association Index (VAI)** across all five models.

- **Semantic Crime Analysis (RQ2):**

  - Analysis of activation texts showed that **Islam most often had the highest proportion of crime-related keywords** (e.g., _terrorism, extremist, violence_) across models.
  - However, variation exists: in GPT2-small and LLaMA3.1-8b, **Hinduism** unexpectedly showed higher crime associations than Islam, reflecting model- and corpus-specific differences.

- **Geographic Associations (RQ3):**

  - Geographic analysis revealed both expected and skewed mappings:

    - Hinduism and Buddhism were strongly tied to **Asia**.
    - Islam was prominent in the **Middle East**.
    - Christianity was strongly linked to **Europe** and **North America**.

  - Africa and South America were underrepresented, while Australia appeared only minimally. This indicates a **Western-centric lens**, shaped more by cultural visibility than by demographic reality.

- **Cross-Model Variation (RQ4):**

  - Larger models (e.g., Gemma-2-9b, Gemma-2-9b-IT) encoded more compact and abstract religious representations, while smaller ones (GPT2-small, LLaMA3.1-8b) showed noisier and sometimes exaggerated associations.
  - This highlights that both **model architecture and training data composition** influence how biases are embedded.

---

## Repository Structure

```bash
SAE_FAIRNESS/
│
├── 0_data_collection_prelim_analysis.ipynb   # Notebook I: Data Collection & Preliminary Analysis
├── 1_semantic_analysis.ipynb                 # Notebook II: Semantic Analysis (crime & geography)
├── 2_sae_religions_feat_overlapp.ipynb       # Notebook III: Latent Feature Overlap Analysis
│
├── step1_fetch_SAE_data_via_inference.py     # Step 1: Fetch SAE activations from Neuronpedia API
├── step2_logits_extractor.py                 # Step 2: Extract logits & explanations
├── step2b_generate_feature_summary.py        # Utility: Generate feature index
├── step3a_check_duplicates_inference.py      # Step 3a: Detect duplicate features
├── step3b_analyze_negative_logits.py         # Step 3b: Analyze negative logits (exploratory)
├── step3b_analyze_positive_logits.py         # Step 3b: Analyze positive logits (exploratory)
├── step4_analyze_duplicate_features_inference.py # Step 4a: Aggregate duplicate feature overlaps
├── step4b_combine_csv_inference.py           # Step 4b: Combine CSV results
├── step5_collect_activation_texts.py         # Step 5: Collect activation texts
├── step6_activation_keyword_analysis.py      # Step 6: Keyword analysis (crime, geography)
├── step8a_count_overlapping_features_intragroup.py  # Step 8a: Intra-group overlaps (RQ1)
├── step8b_count_overlapping_features_intergroup.py  # Step 8b: Inter-group overlaps (RQ2)
├── step8c_count_cosine_sim_intergroup.py     # Step 8c: Cosine similarity (exploratory, not in paper)
│
├── queries7.json                             # Final curated query set
├── keywords.json                             # Keyword sets for semantic analysis
├── requirements.txt                          # Minimal dependencies
├── README.md                                 # This file
|
├── assets/                                  # Static assets for the repository
│   └── htw_logo.png                         # HTW Berlin logo used in README
│
├── archive/                                  # Old experiments & preliminary analysis
│   └── (Contains earlier query sets, analyses, results not in final paper)
│
├── devcontainer/                             # VS Code Devcontainer config
│   └── devcontainer.json
│
├── religion_geo_bar_chart.png                # Geography analysis output figure
└── .env / .gitignore / .ipynb_checkpoints    # Environment & housekeeping
```

---

## Installation & Setup

```bash
# Clone the repository
git clone https://github.com/iug-htw/SAE_fairness.git
cd SAE_fairness

# Create a virtual environment (Python 3.9+)
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
```

### API Keys

This project requires access to:

- **Neuronpedia API** (free, used for SAE feature activations).
- **OpenAI API** (used for some preprocessing and validation tasks).

Create a `.env` file in the repo root:

```bash
OPENAI_API_KEY=your_openai_key_here
NEURONPEDIA_KEY=your_neuronpedia_key_here
```

---

## Notebooks Overview

- **Notebook I – Data Collection & Preliminary Analysis**
  Fetch activations, extract logits, detect duplicate features.

- **Notebook II – Semantic Analysis**
  Probe activations for crime & geography keywords.

- **Notebook III – Overlap Analysis**
  Compute intra- and inter-group overlaps to quantify religion–violence associations.

---

## Archive

The `archive/` folder contains:

- Old experiments with earlier query sets.
- Preliminary analyses not included in the **camera-ready paper**.
- Retained for reproducibility and historical reference.

<!-- ---

## Citation

If you use this code, please cite:

```bibtex
@inproceedings{simbeck2025sae,
...


```
} -->

---

## Credits & Acknowledgments

This research was carried out at HTW Berlin with support from the KIWI Project, whose funding made this work possible.
We also gratefully acknowledge the Neuronpedia API, which provided access to SAE activations and feature explanations.
Their open infrastructure was essential for the experiments conducted in this study.
