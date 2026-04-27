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

  return res.status(err.statusCode || 500).json({
    success: false,
    message: err.message || "Internal Server Error"
  });
};

module.exports = errorMiddleware;