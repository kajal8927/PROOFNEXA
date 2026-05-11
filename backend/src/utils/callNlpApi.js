const axios = require("axios");

const normalizeMatches = (matches) => {
  if (!Array.isArray(matches)) return [];

  return matches.slice(0, 50).map((match) => {
    if (typeof match === "string") {
      return {
        text: match.slice(0, 1000),
        source: "Unknown",
        percentage: 0
      };
    }

    return {
      text: String(match.text || match.matchedText || "").slice(0, 1000),
      source: String(match.source || "Unknown").slice(0, 200),
      percentage: Number(match.percentage || match.score || 0)
    };
  });
};

const callNlpApi = async (text) => {
  if (!process.env.NLP_API_URL) {
    throw new Error("NLP_API_URL is missing in .env file");
  }

  if (!text || text.trim().length < 20) {
    throw new Error("Text is too short for analysis");
  }

  const response = await axios.post(
    process.env.NLP_API_URL,
    {
      text
    },
    {
      timeout: Number(process.env.NLP_API_TIMEOUT) || 30000,
      maxContentLength: 2 * 1024 * 1024,
      maxBodyLength: 2 * 1024 * 1024,
      headers: {
        "Content-Type": "application/json"
      }
    }
  );

  const data = response.data;

  return {
    similarity: Math.min(Math.max(Number(data.similarity || data.similarityScore || 0), 0), 100),
    matches: normalizeMatches(data.matches)
  };
};

module.exports = callNlpApi;