import { useState } from "react";
import { correctGrammar, rewriteText } from "../api";

export default function HomePage() {
  const [inputText, setInputText] = useState("");
  const [outputText, setOutputText] = useState("");
  const [loading, setLoading] = useState(false);

  const handleProcess = async (action) => {
    if (!inputText.trim()) return;

    try {
      setLoading(true);
      setOutputText("");

      let response;

      if (action === "rewrite") {
        response = await rewriteText(inputText);
        setOutputText("✨ Rewritten version:\n\n" + response.data.result);
      }

      if (action === "grammar") {
        response = await correctGrammar(inputText);
        setOutputText("📝 Grammatically corrected:\n\n" + response.data.result);
      }

    } catch (error) {
      console.error(error);
      setOutputText("❌ Error connecting to backend");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-screen bg-[#0f172a] text-white p-6">
      <div className="h-full max-w-7xl mx-auto grid md:grid-cols-2 gap-6 items-stretch">

        {/* LEFT */}
        <div className="bg-[#1e293b] p-6 rounded-2xl flex flex-col min-h-0">
          <h2 className="text-xl mb-4 font-semibold">Your Text</h2>

          <textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Type text..."
            className="flex-1 p-4 rounded-xl bg-[#334155] resize-none overflow-y-auto min-h-0"
          />

          <div className="flex gap-3 mt-4">
            <button
              onClick={() => handleProcess("rewrite")}
              className="flex-1 py-3 rounded-xl bg-blue-500 hover:bg-blue-600"
            >
              Rewrite
            </button>

            <button
              onClick={() => handleProcess("grammar")}
              className="flex-1 py-3 rounded-xl bg-emerald-500 hover:bg-emerald-600"
            >
              Grammify
            </button>
          </div>
        </div>

        {/* RIGHT */}
        <div className="bg-[#1e293b] p-6 rounded-2xl flex flex-col min-h-0">
          <h2 className="text-xl mb-4 font-semibold">Output</h2>

          <div className="flex-1 bg-[#334155] p-4 rounded-xl overflow-y-auto whitespace-pre-wrap min-h-0">
            {loading ? "Processing..." : outputText || "Output appears here"}
          </div>
        </div>

      </div>
    </div>
  );
}