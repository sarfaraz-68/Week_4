import tiktoken

encoding = tiktoken.get_encoding("cl100k_base")

def analyze_text(text):
    tokens = encoding.encode(text)
    token_count = len(tokens)
    price_per_1000_tokens = 0.001
    cost = (token_count / 1000) * price_per_1000_tokens

    print("\nText:", text)
    print("Tokens:", tokens)
    print("Token count:", token_count)
    print("Word count:", len(text.split()))
    print("Example cost: $", cost)

english_text = "I AM WORKING AS AN INTERNEE."
analyze_text(english_text)

rare_word = "antidisestablishmentarianism"
analyze_text(rare_word)

english_sentence = "I am learning artificial intelligence."
urdu_sentence = "میں مصنوعی ذہانت سیکھ رہا ہوں۔"

analyze_text(english_sentence)
analyze_text(urdu_sentence)