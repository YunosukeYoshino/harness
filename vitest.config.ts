import { resolve } from "node:path";
import { defineConfig } from "vitest/config";

export default defineConfig({
  resolve: {
    alias: {
      "@repo/domain": resolve(__dirname, "packages/domain/src/index.ts"),
      "@repo/app": resolve(__dirname, "packages/app/src/index.ts"),
      "@repo/data": resolve(__dirname, "packages/data/src/index.ts"),
      "@repo/integrations": resolve(
        __dirname,
        "packages/integrations/src/index.ts",
      ),
      "@repo/ui": resolve(__dirname, "packages/ui/src/index.tsx"),
      "@repo/shared": resolve(__dirname, "packages/shared/src/index.ts"),
      "@repo/schema": resolve(__dirname, "packages/schema/src/index.ts"),
    },
  },
  test: {
    include: ["packages/*/src/**/*.test.ts"],
    globals: false,
    passWithNoTests: true,
  },
});
