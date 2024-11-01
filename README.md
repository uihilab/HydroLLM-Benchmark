Benchmarking HydroLLM for Hydrology-Specific Question Generation and Answering

This repository contains resources, scripts, and data for benchmarking large language models (LLMs) for hydrology-focused question generation and answering. The project aims to facilitate research and educational applications by developing a domain-specific benchmark dataset and evaluating model performance on hydrology-related tasks.

Project Overview

Objectives

	•	Create a benchmark dataset with various question types (true-false, multiple choice, open-ended, fill-in-the-blank) based on hydrology research articles and textbooks.
	•	Evaluate the performance of LLMs—both general-purpose and domain-specific models—in generating and answering questions relevant to hydrology.
	•	Highlight the importance of domain-specific LLMs for specialized fields like hydrology in research and education.

Key Components

	•	Question Generation: Scripts to generate different types of questions using domain knowledge.
	•	Data Processing: Includes tools for structuring and organizing hydrology data to make it suitable for LLM-based processing.
	•	Evaluation Metrics: Measure the accuracy, relevance, and consistency of responses to hydrology-specific questions.

Repository Structure

	•	Datasets/: Contains benchmark datasets with hydrology questions derived from research materials.
	•	GenerateQA/: Scripts for generating questions and answers, using domain-specific prompts and techniques.
	•	Model Results/: Scripts and data for evaluating and recording model performance on the benchmark dataset.
	•	Resources/: Resources such as hydrology textbooks and research article PDFs, organized by chapters in CSV format.
	•	ChapterDivider.py: Script for separating each chapter of the textbook or article for targeted question generation.
	•	PostProcessData.py: Script to check and re-generate data, ensuring consistency and adherence to desired formats.
	•	getArticleFullText.py: Script to retrieve full-text content from research articles.
	•	post_process.py: Final post-processing script for data cleaning and validation.


Results

The project provides insights into the effectiveness of LLMs in accurately generating and answering hydrology-specific questions. Detailed performance metrics and analysis can be found in the Model Results/ directory.



