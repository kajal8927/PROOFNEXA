const fs = require("fs/promises");
const pdfParse = require("pdf-parse");
const mammoth = require("mammoth");

const extractText = async (filePath, mimeType) => {
  let extractedText = "";

  if (mimeType === "application/pdf") {
    const buffer = await fs.readFile(filePath);
    const data = await pdfParse(buffer);
    extractedText = data.text;
  } 
  else if (
    mimeType ===
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
  ) {
    const result = await mammoth.extractRawText({ path: filePath });
    extractedText = result.value;
  } 
  else if (mimeType === "text/plain") {
    extractedText = await fs.readFile(filePath, "utf-8");
  } 
  else {
    throw new Error("Unsupported file type");
  }

  const cleanedText = extractedText.replace(/\s+/g, " ").trim();

  if (!cleanedText || cleanedText.length < 20) {
    throw new Error("File does not contain enough readable text");
  }

  return cleanedText;
};

module.exports = extractText;