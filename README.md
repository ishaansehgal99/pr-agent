<div align="center">
This fork is modified and used by the Kaito project for its GitHub app. See NOTICE for details.
  
<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://www.qodo.ai/wp-content/uploads/2025/02/PR-Agent-Purple-2.png">
  <source media="(prefers-color-scheme: light)" srcset="https://www.qodo.ai/wp-content/uploads/2025/02/PR-Agent-Purple-2.png">
  <img src="https://codium.ai/images/pr_agent/logo-light.png" alt="logo" width="330">

</picture>
<br/>

[Installation Guide](https://qodo-merge-docs.qodo.ai/installation/) |
[Usage Guide](https://qodo-merge-docs.qodo.ai/usage-guide/) |
[Tools Guide](https://qodo-merge-docs.qodo.ai/tools/) |
[Qodo Merge](https://qodo-merge-docs.qodo.ai/overview/pr_agent_pro/) 💎

PR-Agent aims to help efficiently review and handle pull requests, by providing AI feedback and suggestions
</div>

[![Static Badge](https://img.shields.io/badge/Chrome-Extension-violet)](https://chromewebstore.google.com/detail/qodo-merge-ai-powered-cod/ephlnjeghhogofkifjloamocljapahnl)
[![Static Badge](https://img.shields.io/badge/Pro-App-blue)](https://github.com/apps/qodo-merge-pro/)
[![Static Badge](https://img.shields.io/badge/OpenSource-App-red)](https://github.com/apps/qodo-merge-pro-for-open-source/)
[![Discord](https://badgen.net/badge/icon/discord?icon=discord&label&color=purple)](https://discord.com/invite/SgSxuQ65GF)
<a href="https://github.com/Codium-ai/pr-agent/commits/main">
<img alt="GitHub" src="https://img.shields.io/github/last-commit/Codium-ai/pr-agent/main?style=for-the-badge" height="20">
</a>
</div>

## Table of Contents

- [News and Updates](#news-and-updates)
- [Overview](#overview)
- [Example results](#example-results)
- [Try it now](#try-it-now)
- [Qodo Merge](https://qodo-merge-docs.qodo.ai/overview/pr_agent_pro/)
- [How it works](#how-it-works)
- [Why use PR-Agent?](#why-use-pr-agent)
- [Data privacy](#data-privacy)
- [Contributing](#contributing)
- [Links](#links)

## News and Updates

## May 17, 2025

- v0.29 was [released](https://github.com/qodo-ai/pr-agent/releases)
- `Qodo Merge Pull Request Benchmark` was [released](https://qodo-merge-docs.qodo.ai/pr_benchmark/). This benchmark  evaluates and compares the performance of LLMs in analyzing pull request code.
- `Recent Updates and Future Roadmap` page was added to the [Qodo Merge Docs](https://qodo-merge-docs.qodo.ai/recent_updates/)

## Apr 30, 2025

A new feature is now available in the `/improve` tool for Qodo Merge 💎 - Chat on code suggestions.

<img width="512" alt="image" src="https://codium.ai/images/pr_agent/improve_chat_on_code_suggestions_ask.png" />

Read more about it [here](https://qodo-merge-docs.qodo.ai/tools/improve/#chat-on-code-suggestions).

## Apr 16, 2025

New tool for Qodo Merge 💎 - `/scan_repo_discussions`.

<img width="635" alt="image" src="https://codium.ai/images/pr_agent/scan_repo_discussions_2.png" />

Read more about it [here](https://qodo-merge-docs.qodo.ai/tools/scan_repo_discussions/).

## Overview

<div style="text-align:left;">

Supported commands per platform:

|       |                                                                                                         | GitHub | GitLab | Bitbucket | Azure DevOps |
| ----- |---------------------------------------------------------------------------------------------------------|:------:|:------:|:---------:|:------------:|
| TOOLS | [Review](https://qodo-merge-docs.qodo.ai/tools/review/)                                                 |   ✅   |   ✅   |    ✅     |      ✅      |
|       | [Describe](https://qodo-merge-docs.qodo.ai/tools/describe/)                                             |   ✅   |   ✅   |    ✅     |      ✅      |
|       | [Improve](https://qodo-merge-docs.qodo.ai/tools/improve/)                                               |   ✅   |   ✅   |    ✅     |      ✅      |
|       | [Ask](https://qodo-merge-docs.qodo.ai/tools/ask/)                                                       |   ✅   |   ✅   |    ✅     |      ✅      |
|       | ⮑ [Ask on code lines](https://qodo-merge-docs.qodo.ai/tools/ask/#ask-lines)                             |   ✅   |   ✅   |           |              |
|       | [Update CHANGELOG](https://qodo-merge-docs.qodo.ai/tools/update_changelog/)                             |   ✅   |   ✅   |    ✅     |      ✅      |
|       | [Help Docs](https://qodo-merge-docs.qodo.ai/tools/help_docs/?h=auto#auto-approval)                      |   ✅   |   ✅   |    ✅     |              |
|       | [Ticket Context](https://qodo-merge-docs.qodo.ai/core-abilities/fetching_ticket_context/) 💎            |   ✅   |   ✅   |    ✅     |              |
|       | [Utilizing Best Practices](https://qodo-merge-docs.qodo.ai/tools/improve/#best-practices) 💎            |   ✅   |   ✅   |    ✅     |              |
|       | [PR Chat](https://qodo-merge-docs.qodo.ai/chrome-extension/features/#pr-chat) 💎                        |   ✅   |        |           |              |
|       | [Suggestion Tracking](https://qodo-merge-docs.qodo.ai/tools/improve/#suggestion-tracking) 💎            |   ✅   |   ✅   |           |              |
|       | [CI Feedback](https://qodo-merge-docs.qodo.ai/tools/ci_feedback/) 💎                                    |   ✅   |        |           |              |
|       | [PR Documentation](https://qodo-merge-docs.qodo.ai/tools/documentation/) 💎                             |   ✅   |   ✅   |           |              |
|       | [Custom Labels](https://qodo-merge-docs.qodo.ai/tools/custom_labels/) 💎                                |   ✅   |   ✅   |           |              |
|       | [Analyze](https://qodo-merge-docs.qodo.ai/tools/analyze/) 💎                                            |   ✅   |   ✅   |           |              |
|       | [Similar Code](https://qodo-merge-docs.qodo.ai/tools/similar_code/) 💎                                  |   ✅   |        |           |              |
|       | [Custom Prompt](https://qodo-merge-docs.qodo.ai/tools/custom_prompt/) 💎                                |   ✅   |   ✅   |    ✅     |              |
|       | [Test](https://qodo-merge-docs.qodo.ai/tools/test/) 💎                                                  |   ✅   |   ✅   |           |              |
|       | [Implement](https://qodo-merge-docs.qodo.ai/tools/implement/) 💎                                        |   ✅   |   ✅   |    ✅     |              |
|       | [Scan Repo Discussions](https://qodo-merge-docs.qodo.ai/tools/scan_repo_discussions/) 💎                |   ✅   |        |           |              |
|       | [Auto-Approve](https://qodo-merge-docs.qodo.ai/tools/improve/?h=auto#auto-approval) 💎                  |   ✅   |   ✅   |    ✅     |              |
|       |                                                                                                         |        |        |           |              |
| USAGE | [CLI](https://qodo-merge-docs.qodo.ai/usage-guide/automations_and_usage/#local-repo-cli)                |   ✅   |   ✅   |    ✅     |      ✅      |
|       | [App / webhook](https://qodo-merge-docs.qodo.ai/usage-guide/automations_and_usage/#github-app)          |   ✅   |   ✅   |    ✅     |      ✅      |
|       | [Tagging bot](https://github.com/Codium-ai/pr-agent#try-it-now)                                         |   ✅   |        |           |              |
|       | [Actions](https://qodo-merge-docs.qodo.ai/installation/github/#run-as-a-github-action)                  |   ✅   |   ✅   |    ✅     |      ✅      |
|       |                                                                                                         |        |        |           |              |
| CORE  | [PR compression](https://qodo-merge-docs.qodo.ai/core-abilities/compression_strategy/)                  |   ✅   |   ✅   |    ✅     |      ✅      |
|       | Adaptive and token-aware file patch fitting                                                             |   ✅   |   ✅   |    ✅     |      ✅      |
|       | [Multiple models support](https://qodo-merge-docs.qodo.ai/usage-guide/changing_a_model/)                |   ✅   |   ✅   |    ✅     |      ✅      |
|       | [Local and global metadata](https://qodo-merge-docs.qodo.ai/core-abilities/metadata/)                   |   ✅   |   ✅   |    ✅     |      ✅      |
|       | [Dynamic context](https://qodo-merge-docs.qodo.ai/core-abilities/dynamic_context/)                      |   ✅   |   ✅   |    ✅     |      ✅      |
|       | [Self reflection](https://qodo-merge-docs.qodo.ai/core-abilities/self_reflection/)                      |   ✅   |   ✅   |    ✅     |      ✅      |
|       | [Static code analysis](https://qodo-merge-docs.qodo.ai/core-abilities/static_code_analysis/) 💎         |   ✅   |   ✅   |           |              |
|       | [Global and wiki configurations](https://qodo-merge-docs.qodo.ai/usage-guide/configuration_options/) 💎 |   ✅   |   ✅   |    ✅     |              |
|       | [PR interactive actions](https://www.qodo.ai/images/pr_agent/pr-actions.mp4) 💎                         |   ✅   |   ✅   |           |              |
|       | [Impact Evaluation](https://qodo-merge-docs.qodo.ai/core-abilities/impact_evaluation/) 💎               |   ✅   |   ✅   |           |              |
|       | [Code Validation 💎](https://qodo-merge-docs.qodo.ai/core-abilities/code_validation/)                   |   ✅   |   ✅   |    ✅     |      ✅      |
|       | [Auto Best Practices 💎](https://qodo-merge-docs.qodo.ai/core-abilities/auto_best_practices/)                     |   ✅   |      |         |            |
- 💎 means this feature is available only in [Qodo Merge](https://www.qodo.ai/pricing/)

[//]: # (- Support for additional git providers is described in [here]&#40;./docs/Full_environments.md&#41;)
___

‣ **Auto Description ([`/describe`](https://qodo-merge-docs.qodo.ai/tools/describe/))**: Automatically generating PR description - title, type, summary, code walkthrough and labels.
\
‣ **Auto Review ([`/review`](https://qodo-merge-docs.qodo.ai/tools/review/))**: Adjustable feedback about the PR, possible issues, security concerns, review effort and more.
\
‣ **Code Suggestions ([`/improve`](https://qodo-merge-docs.qodo.ai/tools/improve/))**: Code suggestions for improving the PR.
\
‣ **Question Answering ([`/ask ...`](https://qodo-merge-docs.qodo.ai/tools/ask/))**: Answering free-text questions about the PR.
\
‣ **Update Changelog ([`/update_changelog`](https://qodo-merge-docs.qodo.ai/tools/update_changelog/))**: Automatically updating the CHANGELOG.md file with the PR changes.
\
‣ **Help Docs ([`/help_docs`](https://qodo-merge-docs.qodo.ai/tools/help_docs/))**: Answers a question on any repository by utilizing given documentation.
\
‣ **Add Documentation 💎  ([`/add_docs`](https://qodo-merge-docs.qodo.ai/tools/documentation/))**: Generates documentation to methods/functions/classes that changed in the PR.
\
‣ **Generate Custom Labels 💎 ([`/generate_labels`](https://qodo-merge-docs.qodo.ai/tools/custom_labels/))**: Generates custom labels for the PR, based on specific guidelines defined by the user.
\
‣ **Analyze 💎 ([`/analyze`](https://qodo-merge-docs.qodo.ai/tools/analyze/))**: Identify code components that changed in the PR, and enables to interactively generate tests, docs, and code suggestions for each component.
\
‣ **Test 💎 ([`/test`](https://qodo-merge-docs.qodo.ai/tools/test/))**: Generate tests for a selected component, based on the PR code changes.
\
‣ **Custom Prompt 💎 ([`/custom_prompt`](https://qodo-merge-docs.qodo.ai/tools/custom_prompt/))**: Automatically generates custom suggestions for improving the PR code, based on specific guidelines defined by the user.
\
‣ **Generate Tests 💎 ([`/test component_name`](https://qodo-merge-docs.qodo.ai/tools/test/))**: Generates unit tests for a selected component, based on the PR code changes.
\
‣ **CI Feedback 💎 ([`/checks ci_job`](https://qodo-merge-docs.qodo.ai/tools/ci_feedback/))**: Automatically generates feedback and analysis for a failed CI job.
\
‣ **Similar Code 💎 ([`/find_similar_component`](https://qodo-merge-docs.qodo.ai/tools/similar_code/))**: Retrieves the most similar code components from inside the organization's codebase, or from open-source code.
\
‣ **Implement 💎 ([`/implement`](https://qodo-merge-docs.qodo.ai/tools/implement/))**: Generates implementation code from review suggestions.
___

## Example results

</div>
<h4><a href="https://github.com/Codium-ai/pr-agent/pull/530">/describe</a></h4>
<div align="center">
<p float="center">
<img src="https://www.codium.ai/images/pr_agent/describe_new_short_main.png" width="512">
</p>
</div>
<hr>

<h4><a href="https://github.com/Codium-ai/pr-agent/pull/732#issuecomment-1975099151">/review</a></h4>
<div align="center">
<p float="center">
<kbd>
<img src="https://www.codium.ai/images/pr_agent/review_new_short_main.png" width="512">
</kbd>
</p>
</div>
<hr>

<h4><a href="https://github.com/Codium-ai/pr-agent/pull/732#issuecomment-1975099159">/improve</a></h4>
<div align="center">
<p float="center">
<kbd>
<img src="https://www.codium.ai/images/pr_agent/improve_new_short_main.png" width="512">
</kbd>
</p>
</div>

<div align="left">

</div>
<hr>

## Try it now

Try the Claude Sonnet powered PR-Agent instantly on _your public GitHub repository_. Just mention `@CodiumAI-Agent` and add the desired command in any PR comment. The agent will generate a response based on your command.
For example, add a comment to any pull request with the following text:

```
@CodiumAI-Agent /review
```

and the agent will respond with a review of your PR.

Note that this is a promotional bot, suitable only for initial experimentation.
It does not have 'edit' access to your repo, for example, so it cannot update the PR description or add labels (`@CodiumAI-Agent /describe` will publish PR description as a comment). In addition, the bot cannot be used on private repositories, as it does not have access to the files there.

---

## Qodo Merge 💎

[Qodo Merge](https://www.qodo.ai/pricing/) is a hosted version of PR-Agent, provided by Qodo. It is available for a monthly fee, and provides the following benefits:

1. **Fully managed** - We take care of everything for you - hosting, models, regular updates, and more. Installation is as simple as signing up and adding the Qodo Merge app to your GitHub/GitLab/BitBucket repo.
2. **Improved privacy** - No data will be stored or used to train models. Qodo Merge will employ zero data retention, and will use an OpenAI account with zero data retention.
3. **Improved support** - Qodo Merge users will receive priority support, and will be able to request new features and capabilities.
4. **Extra features** - In addition to the benefits listed above, Qodo Merge will emphasize more customization, and the usage of static code analysis, in addition to LLM logic, to improve results.
See [here](https://qodo-merge-docs.qodo.ai/overview/pr_agent_pro/) for a list of features available in Qodo Merge.

## How it works

The following diagram illustrates PR-Agent tools and their flow:

![PR-Agent Tools](https://www.qodo.ai/images/pr_agent/diagram-v0.9.png)

Check out the [PR Compression strategy](https://qodo-merge-docs.qodo.ai/core-abilities/#pr-compression-strategy) page for more details on how we convert a code diff to a manageable LLM prompt

## Why use PR-Agent?

A reasonable question that can be asked is: `"Why use PR-Agent? What makes it stand out from existing tools?"`

Here are some advantages of PR-Agent:

- We emphasize **real-life practical usage**. Each tool (review, improve, ask, ...) has a single LLM call, no more. We feel that this is critical for realistic team usage - obtaining an answer quickly (~30 seconds) and affordably.
- Our [PR Compression strategy](https://qodo-merge-docs.qodo.ai/core-abilities/#pr-compression-strategy)  is a core ability that enables to effectively tackle both short and long PRs.
- Our JSON prompting strategy enables to have **modular, customizable tools**. For example, the '/review' tool categories can be controlled via the [configuration](pr_agent/settings/configuration.toml) file. Adding additional categories is easy and accessible.
- We support **multiple git providers** (GitHub, GitLab, BitBucket), **multiple ways** to use the tool (CLI, GitHub Action, GitHub App, Docker, ...), and **multiple models** (GPT, Claude, Deepseek, ...)

## Data privacy

### Self-hosted PR-Agent

- If you host PR-Agent with your OpenAI API key, it is between you and OpenAI. You can read their API data privacy policy here:
https://openai.com/enterprise-privacy

### Qodo-hosted Qodo Merge 💎

- When using Qodo Merge 💎, hosted by Qodo, we will not store any of your data, nor will we use it for training. You will also benefit from an OpenAI account with zero data retention.

- For certain clients, Qodo-hosted Qodo Merge will use Qodo’s proprietary models — if this is the case, you will be notified.

- No passive collection of Code and Pull Requests’ data — Qodo Merge will be active only when you invoke it, and it will then extract and analyze only data relevant to the executed command and queried pull request.

### Qodo Merge Chrome extension

- The [Qodo Merge Chrome extension](https://chromewebstore.google.com/detail/qodo-merge-ai-powered-cod/ephlnjeghhogofkifjloamocljapahnl) serves solely to modify the visual appearance of a GitHub PR screen. It does not transmit any user's repo or pull request code. Code is only sent for processing when a user submits a GitHub comment that activates a PR-Agent tool, in accordance with the standard privacy policy of Qodo-Merge.

## Contributing

To contribute to the project, get started by reading our [Contributing Guide](https://github.com/qodo-ai/pr-agent/blob/b09eec265ef7d36c232063f76553efb6b53979ff/CONTRIBUTING.md).

## Links

- Discord community: https://discord.gg/kG35uSHDBc
- Qodo site: https://www.qodo.ai/
- Blog: https://www.qodo.ai/blog/
- Troubleshooting: https://www.qodo.ai/blog/technical-faq-and-troubleshooting/
- Support: support@qodo.ai
