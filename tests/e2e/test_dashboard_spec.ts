import { test, expect } from "@playwright/test";

const BASE = process.env.BASE_URL || "http://localhost:8050";

test.describe("QuickFin dashboard", () => {
  test("loads, analyzes a ticker, and renders charts", async ({ page }) => {
    await page.goto(BASE);
    await expect(page.getByRole("heading", { name: /quickfin/i })).toBeVisible();

    await page.getByPlaceholder(/enter stock ticker/i).fill("AAPL");
    await page.getByRole("button", { name: /analyze/i }).click();

    await expect(page.locator(".assessment-header")).toContainText(/AAPL/i, { timeout: 20000 });
    await expect(page.locator("#radar-chart")).toBeVisible();
    await expect(page.locator("#category-bar-chart")).toBeVisible();

    await page.click('//*[@id="category-bar-chart"]//*[name()="rect" and @class="point"]', { trial: true }).catch(() => {});
    await page.locator(".metric-details").first().waitFor({ state: "visible", timeout: 10000 }).catch(() => {});
  });
});
