const express = require("express");
const authMiddleware = require("../middlewares/auth.middleware");
const {
  getHistory,
  getSubmissionById
} = require("../controllers/history.controller");

const router = express.Router();

router.get("/", authMiddleware, getHistory);
router.get("/:id", authMiddleware, getSubmissionById);

module.exports = router;