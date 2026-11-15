const { test, expect } = require('@playwright/test');

test('research workflow connects to the backend and exposes its results', async ({ page }) => {
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.goto('/');
  await expect(page.getByText('API connected')).toBeVisible();
  await page.getByRole('button', { name: 'Research Workspace', exact: true }).click();
  const request = page.waitForResponse(response => response.url().endsWith('/api/research') && response.request().method() === 'POST');
  await page.getByRole('button', { name: 'Summarize measured spread rates in SAFFIRE' }).click();
  expect((await request).ok()).toBeTruthy();
  await expect(page.getByRole('button', { name: 'Explore analysis' })).toBeVisible();
  await page.getByRole('button', { name: 'Explore analysis' }).click();
  await expect(page.getByRole('heading', { name: 'Measurement summaries' })).toBeVisible();
  await page.getByRole('button', { name: 'Datasets Explorer' }).click();
  await page.getByRole('button', { name: /saffire_runs_cleaned.csv/ }).click();
  await expect(page.getByRole('heading', { name: 'saffire_runs_cleaned.csv profile' })).toBeVisible();
  await page.getByRole('button', { name: 'Investigations', exact: true }).click();
  await expect(page.getByText('NASA PSI · Context').first()).toBeVisible();
  await page.getByRole('button', { name: 'Research Reports' }).click();
  await expect(page.getByRole('heading', { name: 'Research report', exact: true })).toBeVisible();
  expect(errors).toEqual([]);
});

test('mobile navigation opens and switches pages', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/');
  await expect(page.getByText('API connected')).toBeVisible();
  await page.getByRole('button', { name: 'Open navigation' }).click();
  await page.getByRole('button', { name: 'Datasets Explorer' }).click();
  await expect(page.getByRole('heading', { name: 'Dataset files' })).toBeVisible();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBeTruthy();
});


test('evidence explorer traces records, missing values and gravity', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByText('API connected')).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Find the measurements. See the gaps.' })).toBeVisible();
  await page.getByRole('button', { name: 'saffire-1-1', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'saffire-1-1' })).toBeVisible();
  await expect(page.getByText('PDF page 29').first()).toBeVisible();
  await expect(page.getByRole('link', { name: 'Open PDF' }).first()).toHaveAttribute('href', /20170008805.*#page=29/);
  await expect(page.getByText('Missing is not zero')).toBeVisible();
  await expect(page.getByText('16 of the 20 records in this view', { exact: false })).toBeVisible();
  const downloadPromise = page.waitForEvent('download');
  await page.getByRole('button', { name: 'Export visible records' }).click();
  const download = await downloadPromise;
  expect(download.suggestedFilename()).toBe('flare-saffire-runs-evidence.csv');
  const csv = require('fs').readFileSync(await download.path(), 'utf8');
  expect(csv).toContain('saffire-1-1');
  expect(csv).toContain('spread_rate_mm_s');
  await page.getByLabel('Investigation').selectOption('LUCI-RUNS');
  await expect(page.getByText('Simulated lunar gravity').first()).toBeVisible();
  await expect(page.getByRole('button', { name: 'luci-pmma', exact: true })).toBeVisible();
  await page.getByLabel('Show recorded values only').check();
  await expect(page.getByRole('button', { name: 'luci-pmma', exact: true })).toHaveCount(0);
});
