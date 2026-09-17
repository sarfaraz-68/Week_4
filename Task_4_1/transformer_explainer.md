# Transformers, Attention and Context Window

## What is a Transformer?

A Transformer is a neural network architecture that uses attention to understand relationships between tokens.

Before a language model can process text, the text is converted into tokens.

Simple flow:

Text
↓
Tokens
↓
Transformer
↓
Output

## What is Attention?

Attention helps the model decide which tokens are important when processing another token.

For example:

"The student opened the book because he wanted to study."

The model needs to understand the relationship between "he" and "student".

Attention helps the model focus on useful relationships between tokens.

In simple words:

Attention = focusing on important relationships.

## What is a Context Window?

A context window is the amount of tokens that a model can consider at one time.

The context can contain:

- User messages
- Previous conversation
- Instructions
- Other input information

If the input becomes larger than the available context, everything cannot be processed at the same time.

Context is not the same as long-term memory.

Context = information available to the model now.

Memory = information that can be saved and provided again later.

## Why are Transformers Important?

Transformers are the main architecture behind many modern Large Language Models.

They use attention to process relationships between tokens and produce useful predictions or outputs.

## Main Idea

Text
↓
Tokenization
↓
Tokens
↓
Attention
↓
Transformer processing
↓
Output

## What Problem Did Transformers Solve?

Earlier sequence models processed text step by step and could struggle to connect words that were far apart.

Transformers use attention to look at relationships between different parts of the input more effectively.

For example, in a long sentence, attention can help connect a pronoun with the word it refers to, even when the words are separated.