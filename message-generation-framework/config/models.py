"""
Model configuration module.
Contains default configurations for language models.
"""

# Default model configurations
GENERATOR_MODELS = {
    "meta-llama/Llama-3.3-70B-Instruct-Turbo": {
        "provider": "Together AI",
        "description": "Llama 3.3 70B Instruct",
        "default_temperature": 0.7,
        "requires": "together_api_key"
    },
    "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8": {
        "provider": "Together AI",
        "description": "Llama 4 Maverick 17B",
        "default_temperature": 0.7,
        "requires": "together_api_key"
    },
    "google/gemma-2-27b-it": {
        "provider": "Together AI",
        "description": "Google Gemma 2",
        "default_temperature": 0.7,
        "requires": "together_api_key"
    },
    # "anthropic/claude-3-sonnet-20240229": {
    #     "provider": "Together AI",
    #     "description": "Claude 3 Sonnet - Powerful, balanced model for complex tasks",
    #     "default_temperature": 0.7,
    #     "requires": "together_api_key"
    # },
    "gpt-4o": {
        "provider": "OpenAI",
        "description": "GPT-4o",
        "default_temperature": 0.7,
        "requires": "openai_api_key"
    },
    "gpt-4-turbo": {
        "provider": "OpenAI",
        "description": "GPT-4 Turbo",
        "default_temperature": 0.7,
        "requires": "openai_api_key"
    },
    "gpt-3.5-turbo": {
        "provider": "OpenAI",
        "description": "GPT-3.5 Turbo",
        "default_temperature": 0.7,
        "requires": "openai_api_key"
    }
}

EVALUATOR_MODELS = {
    "meta-llama/Llama-3.3-70B-Instruct-Turbo": {
        "provider": "Together AI",
        "description": "Llama 3.3 70B Instruct - Strong evaluation capabilities",
        "default_temperature": 0.2,
        "requires": "together_api_key"
    },
    "gpt-4o": {
        "provider": "OpenAI",
        "description": "GPT-4o - Excellent for detailed evaluation",
        "default_temperature": 0.2,
        "requires": "openai_api_key"
    },
    "gpt-4-turbo": {
        "provider": "OpenAI",
        "description": "GPT-4 Turbo - Strong reasoning for structured evaluation",
        "default_temperature": 0.2,
        "requires": "openai_api_key"
    }
}

# Recommended model pairs
RECOMMENDED_MODEL_PAIRS = [
    {
        "name": "Balanced Performance",
        "generator": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
        "evaluator": "gpt-4o",
        "description": "Generator: Llama 3.3 70B Instruct, Evaluator: GPT-4o"
    },
    {
        "name": "All Together AI",
        "generator": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
        "evaluator": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
        "description": "Both Generator and Evaluator: GPT-4o"
    },
    {
        "name": "All OpenAI",
        "generator": "gpt-4o",
        "evaluator": "gpt-4o",
        "description": "Complete workflow using OpenAI API"
    },
    {
        "name": "Economical Option",
        "generator": "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
        "evaluator": "gpt-3.5-turbo",
        "description": "More economical option with good results"
    }
]