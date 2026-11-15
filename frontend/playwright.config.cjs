const { defineConfig } = require('@playwright/test');
module.exports = defineConfig({
  testDir: './tests',
  timeout: 90000,
  use: {
    baseURL: process.env.FLARE_FRONTEND_URL || 'http://localhost:3000',
    launchOptions: process.env.FLARE_BROWSER_PATH ? { executablePath: process.env.FLARE_BROWSER_PATH } : {},
  },
});
