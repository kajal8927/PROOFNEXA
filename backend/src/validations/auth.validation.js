const validateSignup = ({ name, email, password }) => {
  if (!name || !email || !password) {
    return "Name, email and password are required";
  }

  if (name.trim().length < 2) {
    return "Name must be at least 2 characters";
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  if (!emailRegex.test(email)) {
    return "Please provide a valid email address";
  }

 const strongPassword =
  /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$/;

if (!strongPassword.test(password)) {
  return "Password must include uppercase, lowercase, number and special character";
}

  return null;
};

const validateLogin = ({ email, password }) => {
  if (!email || !password) {
    return "Email and password are required";
  }

  return null;
};

module.exports = {
  validateSignup,
  validateLogin
};