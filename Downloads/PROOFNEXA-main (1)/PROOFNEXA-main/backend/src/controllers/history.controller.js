const Submission = require("../models/Submission");

exports.getHistory = async (req, res, next) => {
  try {
    const page = Math.max(Number(req.query.page) || 1, 1);
    const limit = Math.min(Math.max(Number(req.query.limit) || 10, 1), 50);
    const skip = (page - 1) * limit;

    const filter = {
      userId: req.user._id
    };

    if (req.query.status) {
      filter.status = req.query.status;
    }

    const [submissions, total] = await Promise.all([
      Submission.find(filter)
        .select("-originalText")
        .sort({ createdAt: -1 })
        .skip(skip)
        .limit(limit),
      Submission.countDocuments(filter)
    ]);

    return res.status(200).json({
      success: true,
      message: "History fetched successfully",
      pagination: {
        page,
        limit,
        total,
        totalPages: Math.ceil(total / limit)
      },
      submissions
    });
  } catch (error) {
    next(error);
  }
};

exports.getSubmissionById = async (req, res, next) => {
  try {
    const submission = await Submission.findOne({
      _id: req.params.id,
      userId: req.user._id
    }).select("-originalText");

    if (!submission) {
      return res.status(404).json({
        success: false,
        message: "Submission not found"
      });
    }

    return res.status(200).json({
      success: true,
      message: "Submission fetched successfully",
      submission
    });
  } catch (error) {
    next(error);
  }
};