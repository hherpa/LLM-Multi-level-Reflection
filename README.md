<h1 align="center">🤔 ReAgent</h1>

> [!NOTE]
> This is a research proposal for a new approach to implementing reflective capabilities in LLM agents.

## Demo

https://github.com/user-attachments/assets/7a458b37-7637-4955-b7fc-c95b72755c4d

## Installation

1. Clone the repository:
```bash
git clone https://github.com/hherpa/ReAgent.git
cd ReAgent
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

To start the web interface, run:
```bash
python gradio_app.py
```

The application will be available at http://localhost:7860

## Project Goals

- Creation of a database of reflective judgments for training
- Improving the quality and naturalness of dialogue with LLM agents
- Development of self-analysis and critical thinking abilities

## Architecture

### 1. Initial Response Generation
- The agent receives a query and forms a primary response

### 2. Critical Point Detection
- Analysis of semantic units in the response
- Assignment of confidence level to each unit
- Simulation of mPFC neural activity during information processing

### 3. Critical Point Analysis
- Generation of reflective questions
- Creation of responses in three tones:
  * logical_answer: rational thinking
  * empathic_answer: emotional intelligence
  * skeptic_answer: self-criticism

### 4. Selection
- Selection of the most relevant questions and answers
- Formation of the final set of reflections

### 5. Regeneration
- Improvement of results based on previous iterations
- Integration of different types of thinking

### 6. Validation and Storage
- Saving successful [question:answer] pairs in RAG
- Accumulation of knowledge base for improving reflection 
