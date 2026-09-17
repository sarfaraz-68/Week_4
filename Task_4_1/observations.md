# Task 4.1 — Tokenization Observations

## 1. English Sentence

Text:

"I AM WORKING AS AN INTERNEE."

- Word count: 6
- Token count: 10

### Observation

The sentence contains 6 words but is represented by 10 tokens. This shows that one word does not always equal one token.

---

## 2. Long / Rare Word

Text:

"antidisestablishmentarianism"

- Word count: 1
- Token count: 6

### Observation

The word contains only 1 word, but the tokenizer splits it into 6 tokens. This shows that a single long or uncommon word can be divided into multiple tokens.

---

## 3. English Sentence

Text:

"I am learning artificial intelligence."

- Word count: 5
- Token count: 6

### Observation

The sentence contains 5 words and becomes 6 tokens. The difference happens because tokenization works with pieces of text rather than simply counting complete words.

---

## 4. English vs Urdu

### English

Text:

"I am learning artificial intelligence."

- Word count: 5
- Token count: 6

### Urdu

Text:

"میں مصنوعی ذہانت سیکھ رہا ہوں۔"

- Word count: 6
- Token count: 33

### Observation

The Urdu sentence contains 6 words but becomes 33 tokens, while the English sentence contains 5 words and becomes 6 tokens.

This shows that different languages can use very different numbers of tokens for similar amounts of text. Non-Latin scripts can sometimes require more tokens, which can affect processing and cost in multilingual applications.

---

## 5. Overall Observations

1. Tokens are not the same as words.
2. A single word can be split into multiple tokens.
3. Long or uncommon words can be divided into several tokens.
4. Different languages can produce different token counts.
5. The Urdu example used many more tokens than the English example.
6. Token count matters because LLM context windows are measured in tokens.
7. Token usage can also affect API costs when models are charged based on tokens.

---

## 6. Token Cost Example

The task asks us to understand the connection between token usage and cost.

For a simple estimate, assume a 2,000-word document uses about 2,600 tokens.

Example price:

$0.20 per 1 million input tokens.

Calculation:

2,600 / 1,000,000 × $0.20 = $0.00052

Therefore, the estimated input cost is about:

$0.00052

This is only an example estimate. Actual token counts and prices depend on the model and API being used.

---

## 7. Conclusion

The tokenizer experiment shows that LLMs process text as tokens rather than complete words. The number of tokens depends on the text, word structure, and language.

The experiments also show why tokenization is important for LLMs. Token count affects the amount of text that can fit into a context window and can affect usage costs when using paid APIs.