---
title: "Jekyll Journey: Using Git LFS for Images"
tags: jekyll git
---

# The Plan

I wanted to figure out some way to store images for this blog without bloating the repository size. After doing some research, I discovered [Git LFS](https://git-lfs.com/). This is a Git extension that allows you to store large files in a separate location from the git repo, which is exactly what I was looking for.

**Tl;dr - I got it working!** Here's a picture of my dog Kiwi to prove it:

![Kiwi](/blog/assets/images/2026/05/26/kiwi.jpg)

# The Setup

## 1. Installing Git LFS

I installed `git-lfs` from Homebrew:

```
brew install git-lfs
```

...And then lost my mind for a half hour later on in this process, I'll spare you the details, but the solution was that I needed to run this command in order to start using Git LFS:

```
git lfs install
```

And that's pretty much it for installation! Just **make sure** to run `git lfs install` once, I think whatever documentation I was referencing assumed I already did that, so I was going crazy trying to figure out why it wasn't tracking any files lol. Thankfully this [Stack Overflow post](https://stackoverflow.com/a/74617692) from someone who did the same thing helped me regain my sanity.

## 2. Configuring Git LFS to track files

Next, I needed to configure this repo to track image assets with LFS. This can be done with the `git lfs track` command, e.g.:

```
git lfs track "*.jpg"
```

This will add an entry to the repo's `.gitattributes` file, e.g.:

```gitattributes
*.jpg filter=lfs diff=lfs merge=lfs -text
```

### A brief aside on recursive tracking

Now this is the point where I started losing it because I forgot to run `git lfs install`. I tried a number of things to set it up to recursively track all files under `assets/images/`, that way I could organize them into subdirectories by year/month/day (e.g. `assets/images/2026/05/26/example.jpg`). But since I didn't first run `git lfs install`, Git LFS wasn't tracking anything no matter how I configured it, so I got fed up with it, thinking at the time that the wildcards were the issue ([though it seems folks have difficulties with that too](https://stackoverflow.com/questions/35769330/git-lfs-track-folder-recursively#comment97993905_35769868)). 

So _in theory_, one (or both? lol) of these lines in my `.gitattributes` should be enough to recursively track all files in all subdirectories of `assets/images/`:

```gitattributes
assets/images/** filter=lfs diff=lfs merge=lfs -text
assets/images/**/* filter=lfs diff=lfs merge=lfs -text
```

...but since the wildcards/recursive tracking were a red herring in my troubleshooting, I also ended up adding lines to explicitly track all files ending in several common image file extensions:

```gitattributes
*.jpg filter=lfs diff=lfs merge=lfs -text
*.jpeg filter=lfs diff=lfs merge=lfs -text
*.png filter=lfs diff=lfs merge=lfs -text
*.webp filter=lfs diff=lfs merge=lfs -text
*.gif filter=lfs diff=lfs merge=lfs -text
```

So regardless of if I got the wildcard syntax right or not, I've achieved the desired effect, so I'll just leave it as is for now. I figure that if I end up with images outside the `assets/images/` directory, I'd want those stored in LFS anyway.


## 3. Configuring GitHub Actions to pull files from Git LFS

After all that, Git LFS was now tracking all images files! The final step of this was to update my GitHub Actions workflow to pull LFS files before deploying the blog to GitHub Pages. Thanks to [this GitHub issues comment](https://github.com/orgs/community/discussions/50337), I learned that all I needed to do was update the checkout step in `.github/workflows/jekyll.yml` to include `with -> lfs: true`:

```yaml
...
jobs:
  # Build job
  build:
    ...
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        # ADDED THIS "with" SECTION:
        with:
          # Download Git-LFS files
          # https://github.com/orgs/community/discussions/50337#discussioncomment-5349819
          lfs: true
```

And just like that, my LFS-tracked images were getting pulled in the action and deployed to the GitHub Pages site!

## Footnote 1: Using LFS-tracked images when serving locally

I need to work more with images to make sure I'm understanding this correctly, but in my brief stint setting this up, I noticed that after committing an image that was tracked by Git LFS, the image file was replaced with a pointer file, and this broke the images when serving the blog locally via `jekyll serve`.

To fix this, all I had to do was run:

```
git lfs pull
```

...which pulled the image file from LFS to the local repo in place of the pointer file, and this fixed the issue.

I'll need to figure out my workflow for using image assets on the blog and solidify my understanding of Git LFS as I go. Maybe there's a better way to make it so that the local repo maintains copies of the actual files and only do the whole LFS thing when pushing to remote. Either way, I figured I'd make a note of it here.

## Footnote 2: Image paths

So since I have my site setup to use `/blog` as the `baseurl`, I've found that I need image paths to be prefixed with that in order for Jekyll to find them, e.g. `/blog/assets/images/path/to/file.jpg`.

# Next Steps

Now that I have LFS tracking setup, there's a few more things I need to figure out with how I want to handle images and streamlining that workflow:

- Better scaling/responsiveness with rendered images. Possibly using [rbuchberger/jekyll_picture_tag](https://github.com/rbuchberger/jekyll_picture_tag), I'll have to look into it
- Setup a script to copy an image file to `assets/images/<year>/<month>/<day>/`, creating directories if necessary and defaulting to today's date unless an explicit date is specified, maybe also running `git add` on the newly copied file
- Figure out if I have to run `git lfs pull` each time an image is tracked to get it serving locally, or if there's a better way

# Resources

These proved invaluable when learning about Git LFS and everything else I'd need to get this working:

- ["Learning About Git LFS" by Amy Li](https://medium.com/swlh/learning-about-git-large-file-system-lfs-72e0c86cfbaf)
- [GitHub: Configuring Git Large File Storage](https://docs.github.com/en/repositories/working-with-files/managing-large-files/configuring-git-large-file-storage)
- [GitHub Pages issues post about using LFS files in GH Actions](https://github.com/orgs/community/discussions/50337#discussioncomment-5349819)

# Coming Up:

I took a brief side quest to start setting up some utility scripts for working with this Jekyll blog using Python, so that will probably be the next thing I do a write up on once I've refined that a bit more.
