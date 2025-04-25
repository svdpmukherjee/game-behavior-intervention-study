# Human-in-the-Loop Message Generation Workflow

A Streamlit application for generating, evaluating and refining psychological concept-based messages with human feedback through a Human-in-the-Loop approach.

## Overview

This application helps researchers and practitioners craft messages that closely align with specific psychological concepts. It uses AI language models to generate and evaluate messages, while allowing human experts to provide feedback for refinement. The application follows an iterative process to ensure the messages effectively communicate the intended psychological concept in a natural, conversational manner.

## Features

- **Concept Selection**: Choose from multiple psychological concepts from different theories (Self-Determination Theory, Cognitive Dissonance Theory, Social Norm Theory, Self-Efficacy Theory)
- **Customizable Parameters**: Adjust message focus, tone, style, and length
- **AI-Powered Generation**: Use state-of-the-art language models to generate messages
- **Message Evaluation**: Automatic evaluation of concept alignment with detailed feedback
- **Human Feedback Loop**: Provide structured feedback to guide message refinement
- **Diversity Analysis**: Check similarity between messages to ensure diversity
- **MongoDB Integration**: Store generated messages with metadata for future analysis
- **Multi-Message Workflow**: Generate multiple messages for the same concept with varying parameters

## Technicalities

### Installation

1. Clone the repository:

```bash
git https://github.com/svdpmukherjee/game-behavior-intervention-study.git
cd message-generation-framework
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables (create a `.env` file in the project root):

```
TOGETHER_API_KEY=your_together_api_key
OPENAI_API_KEY=your_openai_api_key
MONGODB_URI=your_mongodb_uri
MONGODB_DB_NAME=message_generator
```

### Usage

1. Start the Streamlit application:

```bash
streamlit run app.py
```

2. Access the application in your web browser at `http://localhost:8501`

3. Follow the workflow:
   - Set up API keys in the sidebar
   - Select a psychological concept
   - Choose task context, message focus, tone, and style
   - Configure message length and number of messages
   - Select generator and evaluator models
   - Enter your user ID
   - Generate and refine messages with feedback
   - View and export final results

### Project Structure

```
.
├── app.py                     # Main Streamlit application
├── requirements.txt           # Project dependencies
├── data/
│   └── concepts.py            # Psychological concepts definitions
├── services/
│   ├── evaluator.py           # Message evaluation service
│   ├── generator.py           # Text generation service
│   ├── mongodb_service.py     # MongoDB storage service
│   └── similarity.py          # Semantic similarity service
├── ui/
│   ├── change_focus.py        # UI for changing message parameters
│   ├── common.py              # Common UI components
│   ├── generation.py          # Message generation view
│   ├── header.py              # Application header
│   ├── next_message.py        # Next message view
│   ├── results.py             # Results view
│   ├── setup.py               # Setup view
│   └── styling.py             # Custom CSS styling
├── workflow/
│   ├── message_workflow.py    # Message generation workflow
│   ├── prompt_builder.py      # Prompt creation for generation
│   └── state_manager.py       # Session state management
└── utils/
    └── helpers.py             # Utility functions
```

### Supported Models

#### Generation Models

- Meta Llama 3.3 70B Instruct (Together AI)
- Meta Llama 4 Maverick 17B (Together AI)
- Google Gemma 2 27B (Together AI)
- GPT-4o (OpenAI)
- GPT-4 Turbo (OpenAI)
- GPT-3.5 Turbo (OpenAI)

#### Evaluation Models

- GPT-4o (OpenAI)
- GPT-4 Turbo (OpenAI)
- GPT-3.5 Turbo (OpenAI)
- Meta Llama 3.3 70B Instruct (Together AI)

### Requirements

- Python 3.8+
- Streamlit
- Sentence Transformers
- OpenAI API key
- Together.ai API key
- MongoDB (optional for message storage)

## Detailed Workflow Process

The application guides you through a structured workflow:

1. **Setup** - Configure parameters for message generation
2. **Generation** - Generate and evaluate messages with AI assistance
3. **Feedback** - Provide expert feedback to refine messages
4. **Next Message** - Choose to continue with same parameters or modify them
5. **Results** - Review and export your finalized messages

### 1. Setup Parameters

The setup screen allows you to configure the following parameters:

#### Psychological Concept Selection

- Choose from concepts grouped by psychological theories (Self-Determination Theory, Cognitive Dissonance Theory, etc.)
- Each concept has a definition that you can edit to match your specific understanding
- Your edited definitions will be saved for future sessions

#### Task Context

- Select from predefined task contexts or create your own
- The task context frames the situation in which your message will be delivered
- Edit existing contexts to better match your specific requirements
- Add new custom contexts using the "Add New Task Context" button

#### Message Characteristics

##### Message Focus

Choose what aspect of the concept to emphasize:

- "The relationship between this concept and maintaining integrity"
- "How this concept manifests in personal growth over time"
- "How this concept helps people overcome specific challenges and obstacles"
- "The universal experience of engaging with this concept"
- "The long-term benefits of applying this concept consistently"
- "How this concept relates to authentic skill development"
- "How this concept guides effective decision-making processes"
- "Practical day-to-day applications of this concept"
- "How this concept shapes perspectives on learning"
- "The relationship between this concept and genuine satisfaction"

##### Message Style

Select the structural format for your message:

- **Question-Answer Format**: Poses questions and provides insightful answers
- **Conditional 'When-Then' Structure**: Uses "when X happens, then Y follows" pattern
- **Comparison or Contrast Structure**: Presents ideas by comparing different approaches
- **Cause-Effect Reasoning Format**: Explains relationships between actions and outcomes

##### Tone

Set the emotional quality and style:

- **Motivational**: Energizing and inspiring
- **Encouraging**: Positive and supportive
- **Informative**: Clear and educational
- **Supportive**: Empathetic and understanding
- **Coaching**: Guiding and instructional
- **Reflective**: Thoughtful and contemplative
- **Straightforward**: Direct and clear
- **Friendly**: Warm and approachable

All of these characteristics can be customized and saved for future use.

##### Message Length

Adjust the number of sentences (1-8) in the generated message:

- **Short** (1-2 sentences): Concise, focused messages
- **Medium** (3-5 sentences): Balanced development of ideas
- **Long** (6-8 sentences): Comprehensive exploration of concepts

##### Message Number

Adjust the number of messages to generate

#### Model Selection

- **Generator Model**: The AI model used to create messages
- **Generator Parameters**: Adjust temperature and top-p settings to control creativity
- **Evaluator Model**: The AI model used to evaluate message alignment
- **Evaluator Parameters**: Configure settings for evaluation accuracy

### 2. Message Generation

After starting the workflow, the AI generates an initial message based on your parameters. Each message goes through:

1. **Generation**: The system creates a message aligned with your selected concept
2. **Evaluation**: The evaluator model assesses how well the message aligns with the target concept
3. **Scoring**: The message receives a percentage score and detailed feedback

The evaluation includes:

- Overall alignment score with the target concept
- Differentiation from competing concepts
- Specific strengths of the message
- Suggested improvements
- Tips for better differentiating from competing concepts

### 3. Providing Feedback

You can interact with each generated message in several ways:

#### Direct Editing

- Edit the message text directly in the text area
- Click "Save & Evaluate" to have the edited message re-evaluated
- Choose whether to count your edit as a new iteration

#### Structured Feedback

- **Rating**: Score the message alignment from 1-10
- **Strengths**: Note aspects that should be preserved
- **Weaknesses**: Identify problems that need addressing
- **Improvement Suggestions**: Provide specific guidance for refinement

#### Action Buttons

- **Refine Message**: Send your feedback to the AI to generate an improved version
- **Accept Message**: Finalize the current message and move to the next one
- **Cancel & Reset**: Start over with new parameters (requires confirmation)

### 4. Diversity Check

The system automatically checks if your new messages are sufficiently different from previously accepted ones:

### 5. Next Message Options

After accepting a message, you can:

- **Use Same Parameters**: Continue with the current settings
- **Change Message Parameters**: Modify focus, style, tone, or length
- Review previously generated messages in the expandable section

### 6. Results & Export

Upon completing your message generation (typically after 3 messages):

- Review all finalized messages
- See a summary of the workflow parameters used
- Export messages as a text file
- Save complete results including all parameters and iterations

### Data Storage

All messages are stored in MongoDB with the following structure:

1. `user_id` - User identifier
2. `concept_name` - Name of the psychological concept
3. `task_context` - Context for the message
4. `message_focus` - Focus area for the message
5. `message_tone` - Tone of the message
6. `message_style` - Style of the message
7. `message_length` - Number of sentences in the message
8. `generator_model` - Model used to generate the message
9. `evaluator_model` - Model used to evaluate the message
10. `iterations` - Number of iterations taken to create the message
11. `message` - The actual message text
12. `evaluation_score` - Score given by the evaluator LLM (0-100)
13. `competing_concepts` - Top competing concepts with their scores
14. `diversity_metrics` - Metrics about message diversity
15. `timestamp` - Time when the message was saved

### Tips for Effective Message Generation

1. **Start with Clear Concept Definitions**: Edit the concept definitions to match your specific understanding
2. **Be Specific in Your Feedback**: Detailed guidance leads to better refinements
3. **Aim for Diversity**: Ensure each message approaches the concept differently
4. **Balance AI and Human Judgment**: The AI evaluation is helpful, but your expertise is crucial
5. **Iterate When Needed**: Don't hesitate to refine messages multiple times to get them right

### Managing Custom Settings

The application allows you to create and manage:

- Custom task contexts
- Custom message focuses
- Custom tones
- Custom message styles

Each of these can be added, edited, and deleted through the respective management sections (look for the 🔧 Manage buttons in each section).

## License

## Contributors

ABC DEF
