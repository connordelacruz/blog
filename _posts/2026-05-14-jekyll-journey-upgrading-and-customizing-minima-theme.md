---
title: "Jekyll Journey: Upgrading and Customizing the Minima Theme"
tags: jekyll
---

After getting this blog up and running, the next step I wanted to take was customizing the theme. Eventually, I want to build a fully custom theme of my own, but for the sake of keeping up momentum I'm settling on just tweaking Minima for now.

# Upgrading to Minima v3

## Part 1: `Gemfile` changes

So out of the box, `jekyll new` creates a project using Minima version 2.5. The first change I wanted to make was to use a dark theme, which is an option with Minima v3's builtin skins. So I set headed to the [jekyll/minima repo](https://github.com/jekyll/minima) to check their documentation.

The first problem: Minima v3 hasn't really been tagged as an official release, so I'd need to update my Gemfile to point to the GitHub repo and reference a specific commit. Doing this, I learned that the README was a little out of date, and the commit referenced in their example was pretty old and didn't support some customizations. So I ended up setting the ref to the most recent commit at time of writing:

```ruby
# Use Minima v3, which is only on GitHub and not tagged or anything for some reason.
gem "minima", github: "jekyll/minima", ref: "4de3223"
```

I also read in Minima's `_config.yml` that it was dependent on the `jekyll-seo-tag` plugin, so I added that to the `:jekyll_plugins` group:

```ruby
group :jekyll_plugins do
  gem "jekyll-feed", "~> 0.12"
  gem "jekyll-seo-tag", "~> 2.9"
end
```

After running `bundle`, all my gems were updated. I also quickly learned that several configs had changed from v2.5 to v3, so the next step was to update my `_config.yml`.

## Part 2: `_config.yml` updates

_(To see all the changes to my config in one place, you can look at the git diff for [this commit](https://github.com/connordelacruz/blog/commit/2d7ef2081f7d704a4bbb2a0684a92813c30e6608#diff-ecec67b0e1d7e17a83587c6d27b6baaaa133f42482b07bd3685c77f34b62d883))_

### `author:`

The first config with syntax changes I noticed was the `email` config, which in v3 is supposed to be nested under `author` along with a config called `name`:

```yaml
author:
  name: Connor de la Cruz
  email: connor.c.delacruz@gmail.com
```

I also removed the `github_username` config, as social link configs have been reworked (more on that in a bit).

### `minima:`

It was at this point that I figured instead of scouring the README for theme configs, I'd take a look at what they had in [Minima's `_config.yml`](https://github.com/jekyll/minima/blob/7e657bf7cace71dbbeddd22297a5ac4e417eb490/_config.yml), and there was actually a goldmine of information here. I ended up copying a lot of the inline comments here into my own file for future reference. I highly recommend using this file as a base if you're looking to customize Minima v3.

After doing a bit of reorganizing, I set a few configs under the `minima` section to use the dark skin and show post excerpts on the homepage:

```yaml
minima:
  skin: dark
  show_excerpts: true
```

I then added my socials to the `social_links` config, and hid the RSS feed link from the list (maybe I'll add it back, but I wanted to keep things simple for now):

```yaml
minima:
  social_links:
    - title: GitHub
      icon: github
      url: "https://github.com/connordelacruz"
    - title: LinkedIn
      icon: linkedin
      url: "https://www.linkedin.com/in/connordelacruz"
    - title: Instagram
      icon: instagram
      url: "https://www.instagram.com/delachrome"
  hide_site_feed_link: true
```

After that, all my socials were linked in the footer with corresponding icons. This was pretty seamless, and there's a ton of icons available. The README says it can use any brand icon from [Font Awesome's CDN](https://fontawesome.com/search?ic=brands).

### `plugins:`

The default Minima config says the theme relies on the following plugins. I still need to learn more about these, but for now I figured I'd just add it to the config if they're required:

```yaml
plugins:
  - jekyll-feed
  - jekyll-seo-tag
```

### `sass:`

So when running `bundle exec jekyll serve`, the output was cluttered with Sass deprecation warnings. Personally I'd prefer to just have the Sass written in a way that _wasn't_ using deprecated syntax, but I'll save that for when I'm building my own theme. For now, I uncommented these lines that came from Minima's config:

```yaml
sass:
  # Disable deprecation warnings from newer versions of sass converter.
  # (Probably just wanna write more compliant sass if/when I make my own theme).
  quiet_deps: true
  silence_deprecations: [import]
```

And like that, I was no longer getting scolded for someone else's deprecated stylesheets lol. 

## Bonus: Favicons

Minima v3 supports adding custom tags to the HTML `<head>` by putting them in `_includes/custom-head.html`. I was able to copy over the `<link>` tags from my personal site and simply update their `href` attributes to pull the favicon files that already exist over there:

`_includes/custom-head.html`:

```html
<!-- Favicon from personal site -->
<link rel="icon" type="image/png" sizes="48x48"   href="https://connordelacruz.com/favicon/icon-48.png">
<link rel="icon" type="image/png" sizes="72x72"   href="https://connordelacruz.com/favicon/icon-72.png">
<link rel="icon" type="image/png" sizes="96x96"   href="https://connordelacruz.com/favicon/icon-96.png">
<link rel="icon" type="image/png" sizes="144x144" href="https://connordelacruz.com/favicon/icon-144.png">
<link rel="icon" type="image/png" sizes="192x192" href="https://connordelacruz.com/favicon/icon-192.png">
<link rel="icon" type="image/png" sizes="512x512" href="https://connordelacruz.com/favicon/icon-512.png">
<link rel="apple-touch-icon"      sizes="180x180" href="https://connordelacruz.com/favicon/apple-touch-icon.png">
```

# Next Steps

I'm reasonably happy with how the blog is looking with minimal changes to the theme. Eventually I want to create a fully original theme to use in place of Minima, but I don't want to get too deep into the weeds on that yet. My priority is to focus on getting the fundamentals up and running and coming up with a workflow so that I actually keep up with writing posts on here. It's a great way to make sure I retain what I learn as I work on this and other projects, and maybe someone else out there will stumble on this and find something specific that ends up being helpful to them! So often I find myself banging my head on my keyboard struggling with some strange esoteric problem or using a poorly documented library, and in those moments its almost always some random blog post from another developer who was kind enough to share their insanely niche discoveries with the world, and I'd love if I could do the same for someone else!

Anyway, here's a few things that I want to tackle next with Jekyll:

- Coming up with a "drafts" workflow, where I can partially write a post and come back to it later without publishing it or causing git conflicts
- Figure out image hosting without bloating the repo, possibly leveraging [git lfs](https://git-lfs.com/)
- Figure out organizing and browsing posts with tags and categories
- Explore what Jekyll plugins are out there
- Setup comment section
- SEO/Analytics stuff

And to get in the rhythm of posting on this blog, I'll probably keep writing these small retrospectives as I go through the process, if only for my sake.
