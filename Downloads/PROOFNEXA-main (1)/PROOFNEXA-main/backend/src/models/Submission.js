const mongoose = require("mongoose");

const matchSchema = new mongoose.Schema(
  {
    text: {
      type: String,
      trim: true
    },
    source: {
      type: String,
      trim: true,
      default: "Unknown"
    },
    percentage: {
      type: Number,
      min: 0,
      max: 100,
      default: 0
    }
  },
  { _id: false }
);

const submissionSchema = new mongoose.Schema(
  {
    userId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "User",
      required: true,
      index: true
    },

    fileName: {
      type: String,
      required: true,
      trim: true
    },

    storedFileName: {
      type: String,
      required: true
    },

    fileType: {
      type: String,
      required: true
    },

    fileSize: {
      type: Number,
      required: true
    },

    originalText: {
      type: String,
      required: true,
      select: false
    },

    textLength: {
      type: Number,
      required: true
    },

    similarityScore: {
      type: Number,
      min: 0,
      max: 100,
      default: 0
    },

    matches: {
      type: [matchSchema],
      default: []
    },

    status: {
      type: String,
      enum: ["uploaded", "processing", "completed", "failed"],
      default: "uploaded",
      index: true
    },

    analyzedAt: {
      type: Date
    },

    errorMessage: {
      type: String
    }
  },
  {
    timestamps: true
  }
);

submissionSchema.index({ userId: 1, createdAt: -1 });
submissionSchema.index({ userId: 1, status: 1 });

module.exports = mongoose.model("Submission", submissionSchema);