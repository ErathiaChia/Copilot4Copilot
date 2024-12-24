# CoPilot for CoPilot

## Purpose
CoPilot for CoPilot is an intelligent decision support system that helps determine the most suitable AI solution for your document processing needs. It uses a conversational interface to guide users through a decision tree, ultimately recommending either:

- Copilot/Amazon Q for Business
- Custom GenAI Solution
- Customized Copilot/Amazon Q
- Ask Your Document Solution Accelerator

## Tech-Stack
- Frontend : Streamlit
- Controller : Python (Decision Tree)
- Model : Ollama (Llama 70B)


## Features
- Decision tree logic to handle complex use case analysis
- Support for various document processing scenarios:
  - Search and Q&A in documents
  - Data visualization
  - Document generation
  - Data extraction
  - Content summarization/analysis
  - Document comparison

## Components
The application consists of three main components:

1. `frontend.py`: Handles the user interface using Streamlit
   - Chat interface
   - Session state management
   - Response display

2. `backend.py`: Manages the AI recommendation engine
   - Integrates with Ollama API
   - Processes user inputs
   - Generates appropriate recommendations

3. `decisiontree.py`: Contains the decision tree logic
   - Manages conversation flow
   - Determines appropriate solutions based on user requirements
   - Handles various use case scenarios

## How It Works

1. Users interact with the chat interface to describe their document processing needs
2. The system classifies the requirement into one of six main categories
3. Follow-up questions are asked based on the initial classification
4. A final recommendation is provided based on the user's specific requirements