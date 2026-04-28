const mongoose = require("mongoose");

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
      required: true
    },

    textLength: {
      type: Number,
      required: true
    },

    similarityScore: {
      type: Number,
      default: 0
    },

    matches: [
      {
        text: String,
        source: String,
        percentage: Number
      }
    ],

    status: {
      type: String,
      enum: ["uploaded", "processing", "completed", "failed"],
      default: "uploaded"
    }
  },
  {
    timestamps: true
  }
);

submissionSchema.index({ userId: 1, createdAt: -1 });

module.exports = mongoose.model("Submission", submissionSchema);