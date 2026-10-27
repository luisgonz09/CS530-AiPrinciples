# CS 530 – AI Principles and Applications

This repository contains coursework, programming exercises, journals, and projects completed for **CS 530 – AI Principles and Applications** as part of the **Master of Science in Computer Science** program at **Southern New Hampshire University (SNHU)**.

Throughout this course, I explored artificial intelligence fundamentals, machine learning, neural networks, natural language processing, and the use of generative AI in software development. The coursework combined written analysis with practical Python exercises to evaluate how AI tools support code generation, debugging, testing, and documentation.

A central focus was the responsible use of AI, including recognizing hallucinations, evaluating generated code, protecting sensitive information, and maintaining human oversight.

---

## Learning Objectives

Throughout this course, I developed practical experience with:

- Artificial intelligence principles and applications
- Supervised, unsupervised, semi-supervised, and reinforcement learning concepts
- Machine learning and deep learning fundamentals
- Neural networks and activation functions
- Natural language processing and large language models
- Prompt engineering and iterative prompt refinement
- Zero-shot and generated knowledge prompting
- AI-assisted code generation and debugging
- Input validation and automated testing
- AI hallucination identification and mitigation
- Hyperparameters and model evaluation concepts
- AI ethics, fairness, transparency, and accountability
- Security, privacy, copyright, and software licensing considerations

---

## Technologies Used

- Python 3
- NumPy
- SciPy
- Pygame
- Python unittest
- JSON
- GitHub Copilot
- OpenAI Codex
- GitHub

---

## Repository Structure

```text
CS530-AiPrinciples/
│
├── 2DPyGame/
│   ├── README.md
│   ├── requirements.txt
│   ├── snake_game.py
│   └── chat.json
│
├── AI_Agents_Exercises/
│   ├── Module Two/
│   ├── Module Three/
│   └── ModuleSeven/
│       ├── task_loader.py
│       ├── test_task_loader.py
│       ├── Activity documentation
│       └── AI interaction log
│
├── CS530Project/
│   ├── CS 530 Project Code Snippet One.py
│   ├── CS 530 Project Code Snippet Two.py
│   ├── generatedCode.py
│   ├── GitHub Copilot evaluation summary
│   └── AI interaction logs
│
├── Journals/
│   └── Written activities and course reflections
│
└── README.md
```

*The structure above highlights the main coursework files and folders. Some file descriptions are abbreviated for readability.*

---

## Major Projects and Activities

### Final Project – GitHub Copilot Evaluation

Evaluated **GitHub Copilot** as an AI development assistant for a fictional organization, **TechNova Solutions**, with healthcare and financial software requirements.

The evaluation examined Copilot’s ability to explain code, identify defects, implement corrections, generate new Python programs, and support testing.

The documented experiments included:

- Debugging a neural network designed to learn XOR
- Reviewing and repairing an employee payroll function
- Generating a single-neuron binary classifier using an OR dataset
- Comparing initial suggestions with results from execution and further review
- Assessing reliability, security, privacy, bias, and licensing concerns

The project concluded with a recommendation for a controlled pilot supported by human review, testing, and organizational safeguards.

### Neural Networks and Binary Classification

Explored neural-network behavior through small Python implementations.

The examples demonstrate:

- Weighted inputs and biases
- Sigmoid and step activation functions
- Forward propagation
- Mean squared error
- Numerical gradient estimation
- L-BFGS-B optimization with SciPy
- Weight updates for single-neuron classification
- The distinction between linearly separable OR data and the XOR problem

These exercises connected machine learning concepts with readable, practical code.

### AI-Assisted Development – Snake Arcade Game

Developed a **Snake-style arcade game using Pygame**, with an accompanying AI interaction log documenting the development process.

Features include:

- Keyboard-controlled movement
- Food collection and scoring
- Timed food and mine spawning
- Self-collision and mine hazards
- Pause and options menu
- Restart and quit controls

The project demonstrates interactive Python programming and the use of AI assistance during application development.

### Prompt Engineering and Debugging Exercises

Used **GitHub Copilot and OpenAI Codex** to investigate how prompt quality affects generated responses.

Activities included:

- Comparing zero-shot and generated knowledge prompting
- Refining requirements for CSV grade processing
- Exploring REST API design, authentication, and authorization
- Reviewing intentionally defective Python code
- Separating code analysis from authorized changes
- Evaluating explanations, assumptions, and proposed corrections

These exercises emphasized clear requirements, explicit constraints, and independent verification.

### Hallucination Mitigation and JSON Task Validation

Examined how incomplete prompts can lead an AI assistant to invent input formats and implementation requirements.

Refined the task into a Python function that reads a JSON task list and returns completed tasks.

The implementation includes:

- Explicit task fields and data types
- File and JSON error handling
- Validation of the top-level data structure
- Filtering of malformed records
- Seven unit tests using temporary files

This activity demonstrates how precise specifications and executable tests help evaluate AI-generated code.

---

## Journals and Written Analysis

The written coursework explores:

- Machine learning paradigms and deep learning
- Ethical AI design and human oversight
- Algorithmic bias, fairness, and explainability
- Intellectual property and open-source licensing
- AI security, privacy, and data integrity
- LLM hallucinations and verification strategies
- Hyperparameters, generalization, and evaluation

These reflections connect technical concepts with the responsibilities involved in developing and adopting AI systems.

---

## Skills Demonstrated

- Python Programming
- AI Tool Evaluation
- Prompt Engineering
- Neural Network Fundamentals
- Numerical Optimization
- AI-Assisted Debugging
- Code Review
- Unit Testing
- Input Validation
- Interactive Game Development
- Security and Privacy Analysis
- Ethical Reasoning
- Technical Documentation

---

## About

This repository serves as part of my academic portfolio while completing my Master of Science in Computer Science. It demonstrates both theoretical understanding and practical exploration of artificial intelligence through programming, experimentation, and written analysis.

The coursework emphasizes evaluating AI output critically, verifying generated code, and retaining human responsibility for software quality and technical decisions.

---

**Author**

**Luis D. Gonzalez Sanchez**

Master of Science in Computer Science  
Southern New Hampshire University
