from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Import models
from models.grammar import correct_long_text
from models.rewrite import rewrite_text
from models.autocomplete import predict_next_tokens

app = FastAPI()

# Enable CORS (needed for React frontend later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schema
class TextRequest(BaseModel):
    text: str


@app.get("/")
def home():
    return {"message": "Writing Assistant Backend Running 🚀"}


@app.post("/grammar")
def grammar_endpoint(req: TextRequest):
    return {"result": correct_long_text(req.text)}


@app.post("/rewrite")
def rewrite_endpoint(req: TextRequest):
    return {"result": rewrite_text(req.text)}


# @app.post("/autocomplete")
# def autocomplete_endpoint(req: TextRequest):
#     suggestions = predict_next_tokens(req.text, top_k=5)
#     return {
#         "input": req.text,
#         "suggestions": suggestions
#     }