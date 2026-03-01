import numpy as np
import sentencepiece as spm
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# -----------------------------
# Config
# -----------------------------
SEQ_LEN = 8
MODEL_PATH = "models/gru_autocomplete_sentencepiece_v2.h5"
SP_MODEL_PATH = "models/sentencepiece_autocomplete_v2.model"

# -----------------------------
# Load tokenizer + model ONCE
# -----------------------------
sp = spm.SentencePieceProcessor()
sp.load(SP_MODEL_PATH)

model = load_model(MODEL_PATH)

VOCAB_SIZE = sp.get_piece_size()

# Stopword blocking
STOP_PIECES = {"▁the", "▁a", "▁an", "▁of", "▁to", "▁in", "▁and"}
STOP_IDS = {sp.piece_to_id(p) for p in STOP_PIECES if sp.piece_to_id(p) != -1}


# -----------------------------
# Top-K prediction function
# -----------------------------
def predict_next_tokens(text: str, top_k: int = 3):
    ids = sp.encode(text, out_type=int)

    if not ids:
        return []

    ids = ids[-SEQ_LEN:]
    ids = pad_sequences([ids], maxlen=SEQ_LEN)

    preds = model.predict(ids, verbose=0)[0]

    # block stopwords
    for sid in STOP_IDS:
        preds[sid] = 0.0

    # get top-k ids
    top_ids = np.argsort(preds)[-top_k:][::-1]

    suggestions = []
    for idx in top_ids:
        piece = sp.id_to_piece(int(idx))
        word = piece.replace("▁", " ").strip()
        if word:
            suggestions.append(word)

    return suggestions