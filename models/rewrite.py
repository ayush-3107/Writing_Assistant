import torch
from transformers import BartTokenizer, BartForConditionalGeneration

# -----------------------------
# Import grammar correction
# -----------------------------
from models.grammar import correct_long_text

# -----------------------------
# Load paraphrasing model ONCE
# -----------------------------
MODEL_NAME = "eugenesiow/bart-paraphrase"

tokenizer = BartTokenizer.from_pretrained(MODEL_NAME)
model = BartForConditionalGeneration.from_pretrained(MODEL_NAME)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()


# -----------------------------
# Paraphrase function
# -----------------------------
def paraphrase_text(text: str) -> str:
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=512
    ).to(device)

    outputs = model.generate(
        **inputs,
        max_length=128,
        num_beams=5,
        do_sample=True,
        temperature=1.8,
        top_p=0.9,
        repetition_penalty=1.2
    )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)


# -----------------------------
# Rewrite pipeline
# -----------------------------
def rewrite_text(text: str) -> str:
    # Step 1: Grammar correction
    corrected_text = correct_long_text(text)

    # Step 2: Tone & fluency improvement
    final_text = paraphrase_text(corrected_text)

    return final_text


# -----------------------------
# Test run
# -----------------------------
if __name__ == "__main__":
    test_text = (
        "Artificial intelligence is rapidly transforming the way people interact with technology. "
    )

    test2="The meeting was conducted in a structured and professional manner, and all key objectives were addressed as planned. However, a few points were, honestly, discussed in a more relaxed way to keep things moving smoothly. The team was kind of satisfied with the overall progress, even though some tasks still need a bit more attention. In the end, everything wrapped up well, and the outcome looked pretty solid"

    print("Original Text:\n", test2)
    print("\nFinal Output:\n")
    print(rewrite_text(test2))
