# HydroLLM-Benchmark

**A Specialized Benchmark Dataset for Hydrology-Focused Question-Answering**

Welcome to **HydroLLM-Benchmark**, a repository dedicated to providing a **benchmark dataset** of hydrology-specific question-answer pairs. This dataset, **generated using AI**, is aimed at supporting research in hydrological modeling, machine learning, and data-driven water resource management. Unlike traditional benchmarks that primarily compare model performances, **our focus here is to introduce a dataset** that can help researchers and practitioners evaluate or develop specialized AI models in hydrology.

## Table of Contents
- [Overview](#overview)
- [Getting Started](#getting-started)
- [Citation](#citation)
- [Feedback](#feedback)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Overview
**HydroLLM-Benchmark** aims to streamline the development of **domain-specific AI solutions in hydrology** by offering a comprehensive benchmark dataset. Through combining foundational textbook content and a large collection of recent hydrology research articles, we created **True/False, Multiple Choice, Fill in the Blanks,** and **Open-Ended** questions. This dataset serves as a **baseline resource** for evaluating or training AI models in hydrology, rather than providing direct comparisons between different models.

- **Datasets/**: Hosts CSV files containing the **AI-generated** questions for hydrological content, categorized by both question type and source type (textbook vs. research article).  
- **GenerateQA/**: Scripts utilized for **automatically generating** the question-answer pairs.  
- **Model Results/**: Example scripts that demonstrate how one might **evaluate** an AI model using this dataset (these are optional and for illustration).  
- **Resources/**: Contains hydrological references like the *Fundamentals of Hydrology* PDF used to generate textbook-based Q&A.  
- **Utility Scripts**: Files (e.g., `ChapterDivider.py`, `post_process.py`) for parsing, data cleaning, or article retrieval.

---

## Getting Started
1. **Clone the Repository**  
   ```bash
   git clone https://github.com/uihilab/HydroLLM-Benchmark.git
   cd HydroLLM-Benchmark
2. **Set Environment Variables**
   ```bash
   api_key = os.get_env("")
   ollama_api = os.get_env("")

## Results

### Fill In The Blanks Q&A Results
![Fill In The Blanks Graph](./Result%20Graphs/FillInTheBlanks.png)
### Multiple Choice Q&A Results
![Multiple Choice Graph](./Result%20Graphs/MultipleChoice.png)
### Open Ended Q&A Results
![Open Ended Graph](./Result%20Graphs/OpenEnded.png)
### True False Q&A Results
![True False Graph](./Result%20Graphs/TrueFalse.png)

## Feedback
We welcome your feedback, suggestions, or any issues you might encounter. Here are a few ways to reach us:
- **Open an Issue**: Submit a [GitHub issue](../../issues) describing your question or concern.
- **Pull Requests**: We encourage contributions that enhance the dataset or improve the scripts.
- **Contact**: Feel free to share ideas or request features through email or our online community.

## License
This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

## Acknowledgements
This benchmark dataset was developed by the [University of Iowa Hydroinformatics Lab (UIHI Lab)](https://hydroinformatics.uiowa.edu/). We extend our gratitude to all contributors and community members who have supported this project, helping to foster innovation at the intersection of hydrology and AI.

> Kizilkaya, D., Sajja, R., Sermet, Y., & Demir, I. (2025). Towards HydroLLM: A Benchmark Dataset for Hydrology-Specific Knowledge Assessment for Large Language Models. DOI: https://doi.org/10.31223/X5R410
