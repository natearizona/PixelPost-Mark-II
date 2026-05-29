# GitHub Preparation

## Requested Repository

- Name: `Pixelpost-Mark-II`
- Visibility: private
- Purpose: digital archaeology and preservation of the Pixelpost photoblogging platform

## Local Status

The local Git repository has been initialized with `main` as the canonical branch.

Initial local branches:

- `main`
- `restoration/first-boot`
- `modernization/future`
- `research/initial-audit`

The initial commit includes repository infrastructure, documentation, policy, and provenance templates.

Recovered historical archives and extracted source trees are intentionally not committed yet. They remain present in the workspace under `archive/original-pixelpost/` pending provenance verification.

Disposable first-boot restoration workspaces are also intentionally untracked under `docker/restoration-workspaces/`.

## GitHub Tooling Status

GitHub CLI is not available in this shell:

```text
$ gh --version
zsh:1: command not found: gh

$ gh auth status
zsh:1: command not found: gh
```

No GitHub remote was created because the repository owner/account and credentials could not be verified from the available environment.

## Required To Create The Private GitHub Repository

One of the following is needed:

- GitHub CLI installed and authenticated with permission to create private repositories.
- A pre-created private GitHub repository URL from the owner account.
- A GitHub token with repository creation permissions and an explicit owner/org target.

## Safe Creation Commands

When GitHub CLI is available and authenticated:

```bash
gh repo create Pixelpost-Mark-II --private --description "Digital archaeology and preservation project for the Pixelpost photoblogging platform"
git remote add origin git@github.com:<owner>/Pixelpost-Mark-II.git
git push -u origin main
git push origin restoration/first-boot modernization/future research/initial-audit
```

Before any push, verify that only preservation infrastructure is tracked:

```bash
git status --short
git ls-files
```

Do not push `archive/original-pixelpost/raw/` or `archive/original-pixelpost/extracted/` until chain-of-custody records are complete.

