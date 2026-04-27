require("dotenv").config();

const express = require("express");
const cors = require("cors");
const helmet = require("helmet");
const morgan = require("morgan");
const rateLimit = require("express-rate-limit");
//const mongoSanitize = require("express-mongo-sanitize");
const hpp = require("hpp");

const authRoutes = require("./routes/auth.routes");
const errorMiddleware = require("./middlewares/error.middleware");
const {
  generalLimiter,
  authLimiter
} = require("./middlewares/rateLimit.middleware");

const app = express();

app.use(helmet());

app.use(
  cors({
    origin: process.env.FRONTEND_URL || "http://localhost:5173",
    credentials: true
  })
);

app.use(express.json({ limit: "1mb" }));
app.use(express.urlencoded({ extended: true, limit: "1mb" }));

//app.use(mongoSanitize());
app.use(hpp());

if (process.env.NODE_ENV === "development") {
  app.use(morgan("dev"));
}

app.use(generalLimiter);

app.get("/", (req, res) => {
  res.status(200).json({
    success: true,
    message: "Plagiarism Detection Backend API is running"
  });
});

app.use("/api/auth", authLimiter, authRoutes);

app.use(errorMiddleware);

app.use((err, req, res, next) => {
  console.error("ERROR:", err);

  res.status(err.statusCode || 500).json({
    success: false,
    message:
      process.env.NODE_ENV === "production"
        ? "Internal server error"
        : err.message
  });
});

module.exports = app;