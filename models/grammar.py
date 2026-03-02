import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration
import re

# -----------------------------
# Load grammar correction model
# -----------------------------
MODEL_NAME = "prithivida/grammar_error_correcter_v1"

tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)
model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()

# -----------------------------
# Grammar correction function
# -----------------------------
def correct_grammar(text: str) -> str:
    """
    Correct grammatical errors in a single sentence or short text.
    """
    if not text or text.strip() == "":
        return text

    input_text = "grammar: " + text

    inputs = tokenizer(
        input_text,
        return_tensors="pt",
        max_length=384,
        truncation=True
    )

    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=128,
            num_beams=5,
            early_stopping=True
        )

    corrected_text = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )
# 🔥 CLEAN PREFIX
    if corrected_text.lower().startswith("grammar:"):
        corrected_text = corrected_text[len("grammar:"):].strip()

    return corrected_text

# -----------------------------
# Capitalization fix function
# -----------------------------
def fix_capitalization(text: str) -> str:
    """
    Capitalize first letter and letters after full stops, exclamation, question marks.
    """
    text = text.strip()
    if not text:
        return text

    # Capitalize first letter
    text = text[0].upper() + text[1:]

    # Capitalize letter after punctuation
    text = re.sub(
        r'([.!?]\s*)([a-z])',
        lambda m: m.group(1) + m.group(2).upper(),
        text
    )

    return text

# -----------------------------
# Sentence-wise correction
# -----------------------------
def correct_long_text(text: str) -> str:
    """
    Corrects a long paragraph by splitting into sentences using simple split.
    Removes empty sentences and fixes capitalization and extra punctuation.
    """
    # Split on ". " but allow multiple punctuation
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())

    # Remove empty sentences
    sentences = [s.strip() for s in sentences if s.strip()]

    corrected_sentences = []
    for s in sentences:
        corrected = correct_grammar(s)
        corrected_sentences.append(corrected)

    # Join sentences with single space
    corrected_text = " ".join(corrected_sentences)

    # Fix capitalization after punctuation
    corrected_text = fix_capitalization(corrected_text)

    # Remove repeated punctuation (e.g., ".." -> ".")
    corrected_text = re.sub(r'([.!?])\1+', r'\1', corrected_text)

    # Ensure paragraph ends with a period
    if not corrected_text.endswith("."):
        corrected_text += "."

    return corrected_text


# -----------------------------
# Example test
# -----------------------------
if __name__ == "__main__":
    test_text = "I am currently working on my final year college project which focus on creating an intelligent writing assistant that help student and profesinals to improve they writing skills. The main idea of this project is to analyse user input text and automaticly correct grammer mistakes while also making the tone more appropriate for academic and professional communication. Many people face difficulty while writing emails, reports, or long assingments because English is not they first language, and this often result in unclear sentences, wrong word usage, and poor expresion of ideas. The system is designed in a way that it take a long paragraph as input and process it through multiple natural language processing components such as tokenization, grametical correction, and tone improvement. First, the text are passed into a grammar correction model which identify common error like missing articles, incorrect verb tenses, and subject verb disagreement, then the corrected output is further refined to improve clarity and readability. One major challange in building this system was selecting a model that is accurate enough but still efficient for real time usage, because some advance models require high computational power and large memory which is not suitable for deployment on low end machines. Another problem was dealing with long input text, since most transformer based models have a fixed maximum token limit and can not process unlimited text at once, so careful handling and truncation was required. Despite these issues, the project aim to provide a practical solution for improving writting quality and reducing common language errors. In future, this system can be expanded to support multiple language, better contextual understanding, and deeper personalization based on user writing habits, which would make it more useful for students, researchers, and working professionals who want to communicate more efectively."
    exp_1="I am currently working on an project and i m facing some difficulties and issues, while implement it."
    exp_2="India is a amazing country."
    exp_3 = "i Am go to market tommorow"
    exp_4=test_text*2
    exp_5 = "I am go to marjet today..I will bing some fruits an vegitables"
    corrected = correct_long_text(exp_5)
    # print("Original:\n", test_text)
    print("\nCorrected:\n", corrected)