# popcat001.github.io

Personal site hosting in-depth AI engineering tutorials.

**Live site: https://popcat001.github.io **

## Tutorials

- [Building Effective Agents](building-effective-agents-tutorial.html)
- [Demystifying Evals for AI Agents](demystifying-evals-ai-agents-tutorial.html)
- [Self-Service Data Analytics with Claude](self-service-data-analytics-tutorial.html)

## Adding a new article

```bash
python add-article.py <filename.html>
```

The script extracts metadata (title, date, read time, source, description) from the HTML file, prompts for anything missing, inserts a card at the top of `index.html`, then optionally commits and pushes.

Built with plain HTML/CSS. No frameworks, no build step.
