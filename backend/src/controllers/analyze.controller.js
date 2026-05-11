const Submission = require("../models/Submission");
const callNlpApi = require("../utils/callNlpApi");

exports.analyzeSubmission = async (req, res, next) => {
  try {
    const { submissionId } = req.params;

    const submission = await Submission.findOne({
      _id: submissionId,
      userId: req.user._id
    }).select("+originalText");

    if (!submission) {
      return res.status(404).json({
        success: false,
        message: "Submission not found"
      });
    }

    if (submission.status === "processing") {
      return res.status(409).json({
        success: false,
        message: "Submission is already processing"
      });
    }

    submission.status = "processing";
    submission.errorMessage = undefined;
    await submission.save();

    try {
      const nlpResult = await callNlpApi(submission.originalText);

      submission.similarityScore = nlpResult.similarity;
      submission.matches = nlpResult.matches;
      submission.status = "completed";
      submission.analyzedAt = new Date();

      await submission.save();

      return res.status(200).json({
        success: true,
        message: "Submission analyzed successfully",
        result: {
          submissionId: submission._id,
          fileName: submission.fileName,
          similarityScore: submission.similarityScore,
          matches: submission.matches,
          status: submission.status,
          analyzedAt: submission.analyzedAt
        }
      });
    } catch (nlpError) {
      submission.status = "failed";
      submission.errorMessage = "NLP analysis failed";
      await submission.save();

      throw nlpError;
    }
  } catch (error) {
    next(error);
  }
};

exports.analyzeRawText = async (req, res, next) => {
  try {
    const { text } = req.body;

    if (!text || text.trim().length < 20) {
      return res.status(400).json({
        success: false,
        message: "Text must be at least 20 characters"
      });
    }

    if (text.length > 50000) {
      return res.status(413).json({
        success: false,
        message: "Text is too large. Maximum 50,000 characters allowed"
      });
    }

    const nlpResult = await callNlpApi(text);

    return res.status(200).json({
      success: true,
      message: "Text analyzed successfully",
      result: {
        similarityScore: nlpResult.similarity,
        matches: nlpResult.matches
      }
    });
  } catch (error) {
    next(error);
  }
};