const express = require("express");
const authMiddleware = require("../middlewares/auth.middleware");
const {
  analyzeSubmission,
  analyzeRawText
} = require("../controllers/analyze.controller");

const router = express.Router();

router.post("/text", authMiddleware, analyzeRawText);
router.post("/:submissionId", authMiddleware, analyzeSubmission);

module.exports = router;