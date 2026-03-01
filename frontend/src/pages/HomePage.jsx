import { useState } from "react";

export default function HomePage() {
  const [inputText, setInputText] = useState("");
  const [outputText, setOutputText] = useState("");
  const [loading, setLoading] = useState(false);

  const simulateProcess = async (action) => {
    if (!inputText.trim()) return;

    setLoading(true);
    setOutputText("");

    await new Promise((res) => setTimeout(res, 1000));

    const processed =
      inputText.replace(/\bi\b/g, "I").replace(/\bim\b/gi, "I'm");

    if (action === "rewrite") {
      setOutputText("✨ Rewritten version:\n\n" + processed);
    }

    if (action === "grammar") {
      setOutputText("📝 Grammatically corrected:\n\n" + processed);
    }

    setLoading(false);
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
                onClick={() => simulateProcess("rewrite")}
                className="flex-1 py-3 rounded-xl bg-blue-500 hover:bg-blue-600"
            >
                Rewrite
            </button>

            <button
                onClick={() => simulateProcess("grammar")}
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