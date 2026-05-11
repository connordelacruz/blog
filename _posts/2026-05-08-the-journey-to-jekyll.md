I've been meaning to get a blog setup on GitHub pages for a while now, and I _finally_ got around to it. Overall, I'm really impressed at how simple it was to get a basic blog up and running! I figure the next step is to actually write something for it, so I figured a good place to start would be to document my experience for posterity, and make some notes on some of the funky stuff I ran into, as well as what I plan to do with this blog moving forward.

So, without further ado...

## Part 1: Where the hell did I leave off?

So a few months ago, I went through [Jekyll's step-by-step tutorial](https://jekyllrb.com/docs/step-by-step/01-setup/) to get familiar with it. It's a really well-structured tutorial, and once I got to the end I thought "Great! Tomorrow I'll start working on my actual blog!"

And then life happened, and I kept kicking the project down the road, until the other day when I had the itch to get back at it. But enough time had passed that I needed to remind myself of some of the hiccups I encountered, and just brush up on concepts in general.

After going through the tutorial and taking notes, I figured it was time to create the project. But I knew that I had run into some issues the first time, and figured I should try and remember what those were by looking at my old tutorial repo.

## Part 2: The setup process

### A note on Ruby versions

This is the first time I've used Ruby for a project, and while I don't remember the exact details from the first time I took a look at Jekyll, I do remember that I had to do a little bit of setup to get the right version of Ruby for the project, especially so that it plays nice with GitHub Actions deployment. The short of it is that I ended up having to do the following:

1. Install [`chruby`](https://github.com/postmodern/chruby) and [`ruby-install`](https://github.com/postmodern/ruby-install)
2. Add the following lines to my `.bashrc`:

    ```bash
    export BREW_ROOT_PATH="$(brew --prefix)"
    ...
    # chruby
    source "$BREW_ROOT_PATH/opt/chruby/share/chruby/chruby.sh"
    # auto-switching with .ruby-version files
    source "$BREW_ROOT_PATH/opt/chruby/share/chruby/auto.sh"
    ```
1. Install the right version by running `ruby-install ruby-3.4.1`
    a. I don't remember the steps to figuring this out, but I landed on version 3.4.1 because it was the most up-to-date version that GitHub Actions also used, at least at time of writing.
2. Run `chruby ruby-3.4.1` before initializing the project with `jekyll new`
3. Add a `.ruby-version` file at the root of the project with `3.4.1` as its contents
4. Finally, add this line to my `Gemfile` to make sure it pulls the version number from `.ruby-version`:

    ```ruby
    # Source ruby version from file
    ruby file: ".ruby-version"
    ```

Then, later on when I was setting up GitHub Actions deployment, I had to make sure to comment out this line in `.github/workflows/jekyll.yml` so that it would pull the Ruby version from `.ruby-version`:

```yaml
jobs:
  # Build job
  build:
    ...
    steps:
      ...
      - name: Setup Ruby
        # https://github.com/ruby/setup-ruby/releases/tag/v1.207.0
        uses: ruby/setup-ruby@4a9ddd6f338a97768b8006bf671dfbad383215f4
        with:
          # ruby-version: '3.1' # Not needed with a .ruby-version file <---- Commented out this line
          ...
```

And after all that, every piece of the puzzle was sourcing `.ruby-version` as a single source of truth!

### Step 1: Creating a Jekyll project

After getting Ruby setup, I ran `chruby ruby-3.4.1` to switch Ruby versions, then created a new project by running `jekyll new <dir-name>`, which creates template files and directories:

```
./
├── _config.yml
├── _posts/
│   └── 2026-05-10-welcome-to-jekyll.markdown
├── 404.html
├── about.markdown
├── Gemfile
├── Gemfile.lock
└── index.markdown
```

The Jekyll tutorial did not have me use `jekyll new` for the example project, and I guess I see why. It pretty much sets up everything you need for a bare minimum functional blog out of the box! It included a default theme called Minima, and a fairly robust `_config.yml` with a ton of inline documentation. I just had to run `bundle exec jekyll serve` and had everything building and served on localhost.

### Step 2: Configuring the project

After getting the new Jekyll project setup, the next step I took was making a few changes to the default `_config.yml`. I filled out the basics like `title`, `description`, `email`, and `github_username` (and commented out `twitter_username` because the goal of making a blog was to get away from social media slop). I also specified some `defaults` so I don't need to specify the layout for posts:

```yaml
defaults:
  - scope:
      path: ""
      type: posts
    values:
      layout: post
  - scope:
      path: ""
    values:
      layout: page
```

And finally, I set `baseurl` and `url` to `"/blog"` and my website URL respectively, which in the next step I learned just magically works when trying to deploy to a GitHub Pages site!

### Step 3: Deployment

For the purpose of getting started with the blog, I basically had everything I needed at this point. So I created a new GitHub repo with a name that matches the `baseurl` config, then followed [Jekyll's docs on GitHub Pages deployment via GitHub Actions](https://jekyllrb.com/docs/continuous-integration/github-actions/).

Apart from commenting out the `ruby-version` line under `jobs > build > steps > with`, I basically mirrored the setup in the docs 1-to-1.

And now, pushing to master automagically builds the Jekyll site and deploys it on https://connordelacruz.com/blog/ !


## What's Next?

So getting things setup to get a simple blog up and running was incredibly straightforward! But there's still plenty of room for growth. Here's a rough outline of what I plan to do next:

- Add a link to my blog on my personal site
- Figure out post tags and setup collections
- Setup analytics
- Install and configure plugins for SEO
- Create a fully custom theme
- Figure out a workflow for writing post drafts
- Figure out a way to host images outside of the main repo to keep it from bloating in size
- Look into some plugins:
    * [jekyll-toc](https://github.com/toshimaru/jekyll-toc)
    * [jekyll-target-blank](https://github.com/keithmifsud/jekyll-target-blank)

...And probably more, but for now I'm happy to have a space on the web where I can post write ups on various topics and projects I'm working on!
