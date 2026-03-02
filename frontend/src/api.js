import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000",
});

export const correctGrammar = (text) =>
  API.post("/grammar", { text });

export const rewriteText = (text) =>
  API.post("/rewrite", { text });