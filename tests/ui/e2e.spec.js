const { test, expect } = require('@playwright/test');

test('Search transaction status', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await page.fill('input[name="search"]', 'TXN000001');
  await page.click('button[type="submit"]');
  await expect(page.locator('.status-badge')).toBeVisible();
});
