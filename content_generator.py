from transformers import pipeline

generator = pipeline("text-generation", model="EleutherAI/gpt-neo-2.7B")
topic_prompt = "Explain the basics of blockchain technology."
response = generator(topic_prompt, max_length=200, num_return_sequences=1)
print(response[0]["generated_text"])
