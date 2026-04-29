const errorMiddleware = (err, req, res, next) => {
  console.error("ERROR:", err);

  if (err.code === 11000) {
    return res.status(409).json({
      success: false,
      message: "Duplicate field value entered"
    });
  }

  if (err.name === "ValidationError") {
    const message = Object.values(err.errors)
      .map((value) => value.message)
      .join(", ");

    return res.status(400).json({
      success: false,
      message
    });
  }

  if (err.name === "CastError") {
    return res.status(400).json({
      success: false,
      message: "Invalid ID format"
    });
  }

  if (err.name === "MulterError") {
    return res.status(400).json({
      success: false,
      message: err.message
    });
  }

  if (err.code === "ECONNREFUSED" || err.code === "ENOTFOUND") {
    return res.status(503).json({
      success: false,
      message: "NLP service is not available"
    });
  }

  if (err.response) {
    return res.status(err.response.status || 502).json({
      success: false,
      message: "NLP service returned an error"
    });
  }

  if (err.code === "ECONNABORTED") {
    return res.status(504).json({
      success: false,
      message: "NLP service timeout"
    });
  }

  return res.status(err.statusCode || 500).json({
    success: false,
    message:
      process.env.NODE_ENV === "production"
        ? "Internal Server Error"
        : err.message || "Internal Server Error"
  });
};

module.exports = errorMiddleware;