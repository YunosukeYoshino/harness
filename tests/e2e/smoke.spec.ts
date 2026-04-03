import { expect, test } from "@playwright/test";

test("web shell renders", async ({ page }) => {
  await page.goto("/");
  await expect(
    page.getByRole("heading", { name: "Agent Harness Starter" }),
  ).toBeVisible();
  await expect(page.getByText("runtime-first テンプレート")).toBeVisible();
});

test("api health responds", async ({ request }) => {
  const response = await request.get("http://127.0.0.1:8787/health");
  expect(response.ok()).toBeTruthy();
  const json = await response.json();
  expect(json).toEqual({
    service: "api",
    status: "ok",
  });
});
