require("dotenv").config();

const express = require("express");
const cors = require("cors");
const helmet = require("helmet");
const morgan = require("morgan");
const hpp = require("hpp");

const authRoutes = require("./routes/auth.routes");
const analyzeRoutes = require("./routes/analyze.routes");
const historyRoutes = require("./routes/history.routes");
const uploadRoutes = require("./routes/upload.routes");

const errorMiddleware = require("./middlewares/error.middleware");
const {
  generalLimiter,
  authLimiter
} = require("./middlewares/rateLimit.middleware");

const app = express();

/**
 * Required for Render / reverse proxy
 * Fixes rate-limit IP issue behind proxy
 */
app.set("trust proxy", 1);

/**
 * Security middleware
 */
app.use(helmet());

/**
 * CORS setup
 */
const allowedOrigins = [
  process.env.FRONTEND_URL,
  "http://localhost:5173",
  "http://localhost:5174",
  "http://localhost:5175",
  "http://localhost:5176"
].filter(Boolean);

app.use(
  cors({
    origin: function (origin, callback) {
      if (!origin || allowedOrigins.includes(origin)) {
        callback(null, true);
      } else {
        callback(new Error("Not allowed by CORS"));
      }
    },
    credentials: true
  })
);

/**
 * Body parser
 */
app.use(express.json({ limit: "1mb" }));
app.use(express.urlencoded({ extended: true, limit: "1mb" }));

/**
 * Prevent HTTP parameter pollution
 */
app.use(hpp());

/**
 * Logger only in development
 */
if (process.env.NODE_ENV === "development") {
  app.use(morgan("dev"));
}

/**
 * General rate limiter
 */
app.use(generalLimiter);

/**
 * Health check route
 */
app.get("/", (req, res) => {
  res.status(200).json({
    success: true,
    message: "Plagiarism Detection Backend API is running"
  });
});

/**
 * API routes
 */
app.use("/api/auth", authLimiter, authRoutes);
app.use("/api/upload", uploadRoutes);
app.use("/api/analyze", analyzeRoutes);
app.use("/api/history", historyRoutes);

/**
 * 404 route
 */
app.use((req, res) => {
  res.status(404).json({
    success: false,
    message: `Route not found: ${req.originalUrl}`
  });
});

/**
 * Custom error middleware
 */
app.use(errorMiddleware);

/**
 * Final error handler
 */
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