# Agent log

Add a dated entry each time you work with your AI coding agent, with the newest entry at the bottom. Each entry records what you asked the agent, what it produced, and what you checked or changed. Paste your key prompts in exactly as you typed them. Include at least one time the agent got something wrong, and how you caught it.

Copy this outline for each entry:

```markdown
## YYYY-MM-DD: What you worked on

- **Asked:** "Paste your prompt here."
- **Agent produced:** What it made or changed.
- **Checked or changed:** How you checked it, and what you fixed.
```

## 2026-11-09: City median sale prices

- **Asked:** “Read AGENTS.md and docs/data_description_sheet.md first.\
Then replace the placeholder index.html with a simple page showing\
the median sale price by city using data/college_town_home_sales.csv.\
Exclude sales under $10,000 and explain that rule on the page.\
Round prices to whole dollars and leave the original data files unchanged.\
Show me the changes for review before creating a pull request.”
- **Agent produced:** A static city/state median table, filtering explanation, reproducible Python generator, and README rebuild instructions. No pull request created.
- **Checked or changed:** Independently recalculated all 18 medians and sale counts; confirmed 35,402 included and 40 excluded sales. SHA-256 checks verified all five source files unchanged. Chromium rendered all 18 rows with no horizontal overflow at 375px. The first browser attempt used an unavailable Playwright browser; switched to installed Chromium and served the page over HTTP after local file navigation was blocked.
