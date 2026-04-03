import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./tests/e2e",
  fullyParallel: false,
  retries: process.env.CI ? 1 : 0,
  reporter: process.env.CI ? "dot" : "list",
  use: {
    baseURL: "http://127.0.0.1:3000",
    trace: "on-first-retry",
  },
  webServer: {
    command: "pnpm build:web && pnpm start:web",
    url: "http://127.0.0.1:3000",
    name: "web",
    timeout: 120_000,
    reuseExistingServer: !process.env.CI,
  },
});
