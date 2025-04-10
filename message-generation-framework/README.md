# Message Generator App - User Guide

https://svdpmukherjee-game-behav-message-generation-frameworkapp-hnwgcs.streamlit.app/

## Overview

The Message Generator App is a human-in-the-loop tool designed to help researchers and practitioners craft messages that closely align with specific psychological concepts. It leverages AI language models to generate and evaluate messages while incorporating your expert feedback throughout the process.

## Getting Started

To use the application, you'll need at least one API key:

- Together AI API key (for models like Llama, Gemma)
- OpenAI API key (for models like GPT-4o, GPT-4-turbo, GPT-3.5-turbo)

Enter your API key(s) in the sidebar to initialize the services.

## Workflow Process

The application guides you through a structured workflow:

1. **Setup** - Configure parameters for message generation
2. **Generation** - Generate and evaluate messages with AI assistance
3. **Feedback** - Provide expert feedback to refine messages
4. **Next Message** - Choose to continue with same parameters or modify them
5. **Results** - Review and export your finalized messages

## 1. Setup Parameters

The setup screen allows you to configure the following parameters:

### Psychological Concept Selection

- Choose from concepts grouped by psychological theories (Self-Determination Theory, Cognitive Dissonance Theory, etc.)
- Each concept has a definition that you can edit to match your specific understanding
- Your edited definitions will be saved for future sessions

### Task Context

- Select from predefined task contexts or create your own
- The task context frames the situation in which your message will be delivered
- Edit existing contexts to better match your specific requirements
- Add new custom contexts using the "Add New Task Context" button

### Message Characteristics

- **Message Focus**: Choose what aspect of the concept to emphasize (e.g., personal growth, overcoming challenges)
- **Message Style**: Select the structure for your message (question-answer, when-then, comparison, cause-effect)
- **Tone**: Set the emotional quality (encouraging, informative, supportive, motivational, etc.)
- **Message Length**: Adjust the number of sentences (1-8) in the generated message
- All of these can be customized and saved for future use

### Model Selection

- **Generator Model**: The AI model used to create messages
- **Generator Parameters**: Adjust temperature and top-p settings to control creativity
- **Evaluator Model**: The AI model used to evaluate message alignment
- **Evaluator Parameters**: Configure settings for evaluation accuracy

## 2. Message Generation

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

## 3. Providing Feedback

You can interact with each generated message in several ways:

### Direct Editing

- Edit the message text directly in the text area
- Click "Save & Evaluate" to have the edited message re-evaluated
- Choose whether to count your edit as a new iteration

### Structured Feedback

- **Rating**: Score the message alignment from 1-10
- **Strengths**: Note aspects that should be preserved
- **Weaknesses**: Identify problems that need addressing
- **Improvement Suggestions**: Provide specific guidance for refinement

### Action Buttons

- **Refine Message**: Send your feedback to the AI to generate an improved version
- **Accept Message**: Finalize the current message and move to the next one
- **Cancel & Reset**: Start over with new parameters (requires confirmation)

## 4. Diversity Check

The system automatically checks if your new messages are sufficiently different from previously accepted ones:

- A similarity analysis compares new messages with accepted ones
- Warning messages appear if a message is too similar to previous ones
- The acceptance button changes to secondary (gray) as a visual cue

## 5. Next Message Options

After accepting a message, you can:

- **Use Same Parameters**: Continue with the current settings
- **Change Message Parameters**: Modify focus, style, tone, or length
- Review previously generated messages in the expandable section

## 6. Results & Export

Upon completing your message generation (typically after 3 messages):

- Review all finalized messages
- See a summary of the workflow parameters used
- Export messages as a text file
- Save complete results including all parameters and iterations

## Tips for Effective Message Generation

1. **Start with Clear Concept Definitions**: Edit the concept definitions to match your specific understanding
2. **Be Specific in Your Feedback**: Detailed guidance leads to better refinements
3. **Aim for Diversity**: Ensure each message approaches the concept differently
4. **Balance AI and Human Judgment**: The AI evaluation is helpful, but your expertise is crucial
5. **Iterate When Needed**: Don't hesitate to refine messages multiple times to get them right

## Managing Custom Settings

The application allows you to create and manage:

- Custom task contexts
- Custom message focuses
- Custom tones
- Custom message styles

Each of these can be added, edited, and deleted through the respective management sections (look for the 🔧 Manage buttons in each section).

## Troubleshooting

- **API Connection Issues**: Verify your API keys are entered correctly
- **Generation Errors**: Check if API usage limits have been reached
- **Saving Problems**: Ensure you have write permissions to the output directories

For more support, contact the development team.
