# Contributing
Documents the rules and processes that govern contributing to this repo.


## Code Workflow
This repo use the [git-flow](https://danielkummer.github.io/git-flow-cheatsheet/)
to manage code. Please familiarize yourself with this workflow. Below are some
of the idioms from the link and some of our internal conventions that are 
codified in this document. You are expected to follow them when working with
code in this repo. Changes to the conventions should be altered in this
governing document.

### Branch naming conventions
Descriptive name of your branches in any of the workflow are expected to
follow the following rules:

1.  name of your branch *MUST* contain only ascii characters from one the
    following sets: `a-z`, `0-9` and `./-`.
2.  the length of the branch must be 50 characters or less (including
    prefix).

### Branch prefixes
Generally whenever you are working with code you are expected to 
work in one of the following branches:

1.  `feature/*`
2.  `hotfix/*`
3.  `bugfix/*`

Where a feature branch is how you add features, hot fixes are for releasing
*EMERGENCY* fixes to production and bug fixes are for fixing bugs
in `develop` branch.

The other prefix that you will use is the `release/*` branch prefix. This
prefix should be used to merge code into both `develop` and `master`.

### Code Reviews
Code reviews are required for *ALL* code that is being merged. Only way to
add code is to merge it down via a `GitHub` Pull Request. Unless we need to 
do some `git` magic to fix issues in our code base.

## Releasing Code
We release from `master` by merging from `develop` via a release branch. We 
test the `develop` branch and deem it releasable. Once this is done we create
a `release/*` branch and merge that down to `master` and `develop`. 

There are two implication of this strategy you should be aware of; `develop` is 
always releasable and `master` is always releasable. You should ensure one 
of the following assumptions in your code that is merged into `develop` or
`master`:

1.  complete
2.  semi-complete, but doesn't break the build
3.  not complete but isolated enough that it will not break the build

Basically *DON'T* break the build!

Example of how a release **SHOULD** be made:

1.  generate a release number for your release (see below for more info)
2.  create a release candidate by branching from `develop` and naming your
    branch `release/REL-VERSION`.
3.  update the `CHANGELOG.md` file with the release number and any
    documentation you need to include in this release.
4.  create 2 pull requests with your release branch against `develop` 
    and `master`
5.  announce the pull requests code review to the team, get an approval for
    merge.
6.  when the release branch is merged into `master` tag the master branch
    and push up the tag up to origin.


### Generating release number
We follow a simple semantic release versioning. 

```
    {MAJOR-VERSION-NUMBER}.{MINOR-VERSION-NUMBER}.{BUG/HOT-FIX-NUMBER}
```

Generally, you would increment any of these based on latest release or
reset any of these values to 0 once you've bumped up one of the bases.

You should either find the latest release number or ask the team what was the 
latest release. Once that has been established you can increment one of its
sub part based on your particular situation and create a new release number.

## Tagging a release
You must tag a release that was merged into master.

Example

```bash
    $ git tag -a v0.1.0 -m "description of the release"
    $ git push origin v0.1.0
```
