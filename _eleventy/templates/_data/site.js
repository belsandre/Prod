module.exports = {
  username: process.env.SITE_USERNAME || "user",
  year: new Date().getFullYear(),
  buildDate: new Date().toISOString()
};
