# Collation

## Compacted Summaries

Throughout the documents many external references are made to good standards. E.g. in the form of blogs written for humans or verbose standards meant for specificity.

The job of the collator is to go through these referenced documents, compact and summarize them into the [summaries](../summaries) directory, and create links to them at the location of original reference.

References should look like this (the summary path is relative to the document containing the reference, typically from the project root):

```markdown
Use this git commit message advice in this [post](https://chris.beams.io/git-commit) ([summary](./summaries/git-commit-messages-chris-beams.md))
```

## Drop-In AGENTS.md Template

There is an [AGENTS.md template](../agents_md_template.md) that should be kept up to date which you can drop into a project's `AGENTS.md` that will then follow this repository's guidelines.

As part of this process go and update it if necessary.
