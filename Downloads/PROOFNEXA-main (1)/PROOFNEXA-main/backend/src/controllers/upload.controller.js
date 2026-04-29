const fs = require("fs/promises");
const Submission = require("../models/Submission");
const extractText = require("../utils/extractText");

exports.uploadFile = async (req, res, next) => {
  let uploadedFilePath;

  try {
    if (!req.file) {
      return res.status(400).json({
        success: false,
        message: "File is required"
      });
    }

    uploadedFilePath = req.file.path;

    const extractedText = await extractText(
      req.file.path,
      req.file.mimetype
    );

    const submission = await Submission.create({
      userId: req.user._id,
      fileName: req.file.originalname,
      storedFileName: req.file.filename,
      fileType: req.file.mimetype,
      fileSize: req.file.size,
      originalText: extractedText,
      textLength: extractedText.length,
      status: "uploaded"
    });

    return res.status(201).json({
      success: true,
      message: "File uploaded and text extracted successfully",
      submission: {
        id: submission._id,
        fileName: submission.fileName,
        fileType: submission.fileType,
        fileSize: submission.fileSize,
        textLength: submission.textLength,
        status: submission.status,
        createdAt: submission.createdAt
      },
      extractedTextPreview: extractedText.substring(0, 300)
    });
  } catch (error) {
    if (uploadedFilePath) {
      await fs.unlink(uploadedFilePath).catch(() => {});
    }

    next(error);
  }
};