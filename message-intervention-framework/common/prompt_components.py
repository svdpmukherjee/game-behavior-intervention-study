"""Module containing prompt components for message generation and evaluation."""

# Generator prompt components

DEFAULT_GENERATION_PROMPT = """
Context: {context}

I need you to craft a message that strongly aligns with the psychological construct of {construct_name}.

Here is the detailed description of {construct_name}:
{construct_description}

Here are examples of messages that exemplify {construct_name}:
{construct_examples}

This construct is differentiated from other constructs in these ways:
{construct_differentiation}

{generation_instruction}

Create exactly one message that is 3-4 sentences long, using simple, conversational and natural language at approximately an 8th-grade reading level. Use short sentences and avoid complex vocabulary, long words, jargon, or academic phrasing. The message should be easily understood by the average person while still conveying the core principles of {construct_name}.

IMPORTANT: Keep each sentence short for better readability. Break longer ideas into multiple short sentences.

The message should encourage honest effort and authentic skill development, rather than taking shortcuts or using unauthorized assistance.
"""

DIVERSITY_GENERATION_PROMPT = """
Context: {context}

I need you to craft a message that strongly aligns with the psychological construct of {construct_name}, but approaches it from a unique angle.

Here is the detailed description of {construct_name}:
{construct_description}

Here are examples of messages that exemplify {construct_name}:
{construct_examples}

This construct is differentiated from other constructs in these ways:
{construct_differentiation}

{generation_instruction}

IMPORTANT DIVERSITY GUIDANCE:
- Use a different approach than typical messages about this construct
- Focus on {diversity_focus}
- Avoid common phrasings or standard motivational language
- Create a message that feels distinctly different from other messages about this construct
- Still maintain perfect alignment with the core principles of {construct_name}

Create exactly one message that is 3-4 sentences long, using simple, conversational and natural language at approximately an 8th-grade reading level. Use short sentences and avoid complex vocabulary, long words, jargon, or academic phrasing. The message should be easily understood by the average person while still conveying the core principles of {construct_name}.

IMPORTANT: Keep each sentence short for better readability. Break longer ideas into multiple short sentences.

The message should encourage honest effort and authentic skill development, rather than taking shortcuts or using unauthorized assistance.
"""

IMPROVEMENT_PROMPT = """
Current message: "{current_message}"
Current alignment score: {current_score}%

Context: {context}

Instruction: {generation_instruction}

The message aligns with the construct, but to reach a higher score (90%+), focus on these specific improvements:

1. {score_improvement_strategy}
2. Better differentiate from {top_competing_construct} by: {differentiation_tip}
3. Ensure the message remains concise (3-4 sentences) and natural
4. Make sure it encourages honest effort and authentic skill development

IMPORTANT: Keep each sentence short for better readability. Break longer ideas into multiple short sentences.

{conservatism_guidance}

Provide the improved message only.
"""

CLOSE_TO_TARGET_PROMPT = """
Current message: "{current_message}"
Current alignment score: {current_score}%
Target score: {target_score_threshold}%

Context: {context}

Instruction: {generation_instruction}

To push this message over the target threshold of {target_score_threshold}%, focus on these specific improvements:

1. {score_improvement_strategy}
2. Better differentiate from {top_competing_construct} by: {differentiation_tip}
3. Ensure the message remains concise (3-4 sentences) and natural
4. Make sure it encourages honest effort and authentic skill development

IMPORTANT: Keep each sentence short for better readability. Break longer ideas into multiple short sentences.

Provide the improved message only.
"""

STANDARD_IMPROVEMENT_PROMPT = """
Current message: "{current_message}"

Context: {context}

Instruction: {generation_instruction}

Focus on these improvements:

1. {score_improvement_strategy}
2. {differentiation_guidance}
3. Keep the message concise (3-4 sentences) and natural
4. Ensure it encourages honest effort and authentic skill development

IMPORTANT: Keep each sentence short for better readability. Break longer ideas into multiple short sentences.

Provide the improved message only.
"""



# Evaluator prompt components

AUGMENTED_EVALUATION_PROMPT = """
Context: {context}

Message to evaluate: "{message}"

Target Construct: {construct_name}

Construct Description: {construct_description}

Construct Examples: {examples}

Construct Differentiation: {differentiation}

SCORING GUIDELINES:
- Be precise and granular in your scoring. Messages with slightly different quality should receive different scores.
- Consider each message in isolation without comparing to previous iterations
- For each criterion, provide a specific score explanation with evidence from the message
- Maintain the same standards across all evaluations
- Focus on textual evidence rather than inferences
- Even small improvements in alignment should be reflected in score increases

IMPORTANT EVALUATION GUIDELINES:
- Maintain consistency in your evaluation approach across messages
- When a message aligns strongly with the target construct, ensure competing constructs receive proportionally lower scores
- Be disciplined about score differences - they should reflect meaningful distinctions between constructs
- Avoid score inflation for non-target constructs that only tangentially relate to the message
- A message scoring 85-89% shows strong alignment but has room for improvement
- A message scoring 90-94% demonstrates exceptional alignment with nearly all key aspects
- A message scoring 95-100% must demonstrate perfect alignment with all key aspects without any elements of competing constructs

Evaluate how well this message aligns with the target construct using these five criteria:

1. Core Element Alignment: Does the message capture the essential psychological mechanism of the construct?
2. Differentiation: Does the message avoid elements explicitly differentiated from this construct?
3. Language Appropriateness: Does the message use natural, motivational language suitable for task completion?
4. Conciseness: Is the message 3-4 sentences, focused, simple and have short sentences?
5. Ethical Dimension: Does the message encourage honest effort and authentic skill development?

SCORING RUBRIC:
- 95-100%: Message perfectly captures all aspects of the construct with ideal emphasis while completely avoiding elements of differentiated constructs. Message uses natural language that precisely captures the psychological mechanism and perfectly resembles the provided examples.

- 90-94%: Message excellently captures nearly all aspects of the construct with appropriate emphasis while clearly avoiding most elements of differentiated constructs. Message uses language that very clearly captures the psychological mechanism and closely resembles the provided examples.

- 85-89%: Message strongly captures most aspects of the construct with good emphasis while avoiding important elements of differentiated constructs. Message uses language that clearly captures the psychological mechanism and resembles the provided examples well.

- 80-84%: Message clearly captures several key aspects of the construct and largely avoids elements of differentiated constructs. Message contains similar themes to the examples with only minimal overlap with related constructs.

- 75-79%: Message adequately captures some important aspects of the construct but may include minor elements from differentiated constructs. Message shows similarity to examples but lacks precision in differentiating from other constructs.

- 70-74%: Message conveys basic aspects of the construct but includes elements from one or two differentiated constructs. Message shows general similarity to examples but lacks precision.

- 60-69%: Message only partially relates to the construct description and fails to maintain boundaries from multiple differentiated constructs. Message has limited similarity to examples.

- 50-59%: Message tangentially relates to the construct description but primarily reflects aspects of differentiated constructs. Message has minimal similarity to examples.

- 0-49%: Message contradicts the construct description or primarily exemplifies differentiated constructs. Message bears little resemblance to provided examples.

First, provide a detailed score (0-100%) for the target construct with specific reasoning based on the criteria and rubric above.

Then provide explicit feedback on what specific changes would improve the score by 5-10%.

Next, score ALL the listed psychological constructs:
{construct_list}

Present your scores in this format:
### Construct Confidence Scores
- Construct1: XX%
- Construct2: XX%
[all constructs]

Then provide structured feedback in this JSON format:
{{
    "context": "Specific context improvement to better target the construct",
    "generation_instruction": "Specific guidance for message generation improvement",
    "top_competing_construct": "Name of the most similar competing construct",
    "differentiation_tip": "Specific tip to better differentiate from the top competing construct",
    "score_improvement_strategy": "Explicit changes needed to improve score by 5-10%",
    "conciseness_tip": "Guidance to make the message more concise if needed"
}}
"""