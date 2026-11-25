# popcat001.github.io

Personal site hosting in-depth AI engineering tutorials.

**Live site: https://popcat001.github.io **

## Tutorials

- [Building Effective Agents](building-effective-agents-tutorial.html)
- [Demystifying Evals for AI Agents](demystifying-evals-ai-agents-tutorial.html)
- [Self-Service Data Analytics with Claude](self-service-data-analytics-tutorial.html)
- [How the Claude Code Team Does Code Review](code-review-at-anthropic-tutorial.html)
- [Claude Ship: Anthropic Wants Claude to Get Your PRs Merged, Too](introducing-claude-ship-en.html)
- [Anthropic 推出 Claude Ship 测试版](introducing-claude-ship.html) (中文)

## Adding a new article

```bash
python add-article.py <filename.html>
```

The script extracts metadata (title, date, read time, source, description) from the HTML file, prompts for anything missing, inserts a card at the top of `index.html`, then optionally commits and pushes. If the article HTML does not already load Google Analytics 4, the script inserts the standard gtag.js snippet for `G-67RQCF9R6K` at the top of `<head>`.

Built with plain HTML/CSS. No frameworks, no build step.
