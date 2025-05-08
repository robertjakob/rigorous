# Model Configuration Guide

This guide explains how to configure different AI models for use with the Manuscript Reviewer system.

## Default Configuration

By default, the system uses ChatGPT 3.5 Turbo (`gpt-3.5-turbo`), which provides a good balance between performance and cost. However, for more sophisticated analysis, you may want to use more powerful models like GPT-4.

## Available Models

Here are some models you can use with this system:

| Model | Description | Pros | Cons |
|-------|-------------|------|------|
| `gpt-3.5-turbo` | Default model | Fast, cost-effective | Less sophisticated analysis |
| `gpt-4` | More powerful model | More accurate, better reasoning | Slower, more expensive |
| `gpt-4-turbo` | Updated GPT-4 | Newer capabilities, faster than GPT-4 | More expensive than GPT-3.5 |
| `claude-3-opus-20240229` | Claude 3 Opus | Alternative to GPT-4, different strengths | Requires Anthropic API key |
| `claude-3-sonnet-20240229` | Claude 3 Sonnet | Good balance of performance and speed | Requires Anthropic API key |

## Setting Up Your API Keys

### OpenAI API Keys

1. Create an account at [OpenAI](https://platform.openai.com/signup)
2. Navigate to the [API Keys page](https://platform.openai.com/api-keys)
3. Create a new API key
4. Copy the key to your `.env` file (see below)

### Anthropic API Keys (for Claude models)

1. Create an account at [Anthropic](https://console.anthropic.com/signup)
2. Navigate to the API Keys section
3. Create a new API key
4. Copy the key to your `.env` file (see below)

## Configuring Your Model

### Using the `.env` File

1. Open the `.env` file in the root directory of the project
2. Update the `OPENAI_API_KEY` with your API key
3. Change the `DEFAULT_MODEL` to your preferred model

Example `.env` file for OpenAI GPT-4:

```
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Model Configuration
DEFAULT_MODEL=gpt-4
```

Example `.env` file for Anthropic Claude:

```
# Anthropic API Configuration
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Model Configuration
DEFAULT_MODEL=claude-3-opus-20240229
```

### Command Line Configuration

You can also specify the model when running the analysis:

```bash
# For OpenAI models
python run_analysis.py --model gpt-4

# For Anthropic models
python run_analysis.py --model claude-3-sonnet-20240229
```

## Performance Considerations

- **GPT-4** generally provides the most thorough analysis but can be slower and more expensive
- **GPT-3.5 Turbo** is much faster and cheaper, but may miss subtle issues
- **Claude 3 models** provide a good alternative to OpenAI models with different strengths

## Cost Management

Running these models incurs costs based on the number of tokens processed:

| Model | Approximate Cost per Full Paper Analysis |
|-------|------------------------------------------|
| GPT-3.5 Turbo | $0.10 - $0.25 |
| GPT-4 | $0.75 - $2.00 |
| GPT-4 Turbo | $0.40 - $1.00 |
| Claude 3 Opus | $0.80 - $2.20 |
| Claude 3 Sonnet | $0.30 - $0.80 |

Costs vary based on manuscript length and complexity.

## Troubleshooting

- If you encounter `API key not valid` errors, check that you've correctly copied your API key
- If you get `Model not found` errors, ensure you're using a valid model identifier
- For rate limit errors, you may need to wait or switch to a different model

## Need Help?

If you need assistance with model configuration, please:
- Check the [GitHub repository](https://github.com/robertjakob/rigorous) for updates
- Open an issue on GitHub for technical problems
- Contact us at rjakob@ethz.ch for specific questions 