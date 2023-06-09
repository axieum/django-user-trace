# Contributing

## Discussions

[Discussions][github:discussions] are a great way to ask for help without
undergoing the formalities of opening an issue. You are encouraged to use
discussions where appropriate.

* With a single question, you show where contributors can improve the user
  experience

## Issues

[Issues][github:issues] are an invaluable asset to the success of this project.

* Ideas enable others to make meaningful contributions
* Problems highlight where this project is lacking
* Issues can help others debug their problems

Thank you for creating them.

## Pull Requests

[Pull requests][github:prs] are the best way to get your ideas into this
repository's codebase.

When deciding to merge a pull request, the following things are taken into
account:

#### 1. Does it state intent

You should be clear with which problem you are trying to solve within your
contribution.

#### 2. Is it justified

You should justify the way your change solves the problem, i.e. why this change
is better. It may also be worth mentioning any alternate solutions considered
but discarded.

#### 3. Is it of quality

There are no grammatical or spelling mistakes - it reads well.

Try to make sure your explanation can be understood without external resources.

Instead of giving a URL to a discussion, try to summarise the relevant points.

## Branches

A branch contains commits to be included in an aforementioned
[pull request](#pull-requests).

### Branching Strategy

This project follows the [GitHub flow][github:flow] - a lightweight,
branch-based workflow that supports teams and projects where deployments are
made regularly.

#### `main`

At any given time, the latest code that exists in production can be found under
the `main` branch.

#### `beta` / `alpha`

The latest Beta and Alpha releases can be found under the `beta` and `alpha`
branches respectively. Their corresponding versions contain the `-beta`
or `-alpha` suffixes.

#### `+([0-9])?(.{+([0-9]),x}).x`

Branches that match the given pattern are for maintenance releases, generally
used for patching older versions of the codebase as outlined below.

## Commits

Many commits may form an aforementioned pull request.

### Commit Messages

This project adheres to [Conventional Commits][conventionalcommits] - a
specification for adding human and machine-readable meaning to commit messages.

It is worth noting that your commit messages will be used to build automated
[changelogs][changelog]! Hence, code owners may choose to squash your commits in
any pull requests to ensure they meet our standards outlined in the
aforementioned Conventional Commits.

## Versions

This project follows the [Semantic Versioning][semver] specification.

### Major Releases

A new feature or fix may introduce a breaking change, this warrants a new major
version. These releases are not backwards compatible.

### Pre-releases

As new features and breaking changes are developed, we may decide to deploy
these only to our most dedicated users to get feedback. These releases are
identified by a `-beta` or `-alpha` suffix in the version specifier.

### Maintenance Releases

Often, it makes sense to release important patches to older versions so those
who cannot update due to strict policies may benefit. To track an older major
version, look for its related branch that follows the
pattern `+([0-9])?(.{+([0-9]),x}).x`, e.g. `2.x`.

## Continuous Integration & Deployment (CI/CD)

This project uses [GitHub Actions][github:actions] in tandem with
[release-please][release-please] to automate building, testing and deploying new
versions of the codebase.

### How it works?

When new commits make their way into one of the release branches outlined in the
[Branching Strategy](#branching-strategy), a GitHub [workflow][workflow:release]
is triggered. This workflow in turn executes [release-please][release-please].

[changelog]: CHANGELOG.md
[conventionalcommits]: https://www.conventionalcommits.org/
[github:actions]: https://github.com/features/actions
[github:discussions]: https://github.com/axieum/django-user-trace/discussions
[github:flow]: https://guides.github.com/introduction/flow
[github:issues]: https://github.com/axieum/django-user-trace/issues
[github:prs]: https://github.com/axieum/django-user-trace/pulls
[release-please]: https://github.com/googleapis/release-please
[semver]: https://semver.org/
[workflow:release]: .github/workflows/release.yml
