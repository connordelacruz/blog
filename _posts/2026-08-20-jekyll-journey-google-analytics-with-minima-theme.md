---
title: "Jekyll Journey: Google Analytics with Minima Theme"
tags: jekyll
---

So I've recently linked to this blog on my personal website, so I figured now was a good time to setup Google Analytics. This is a short one, but I figured I'd post it because I didn't realize how easy this part would be.

## My initial (wrong) approach

I initially figured I'd try the plugin `jekyll-analytics`. That's the first thing that comes up when searching "jekyll google analytics", and I mean the first result on Google is always right! Right?

I installed it and configured it, but ran into issues where it was telling me my Google Analytics ID was in an invalid format. It was expecting the legacy ID that was prefixed with "UA-", but I was using a newly created ID that's prefixed with "G-", which it did not like.

I realized then that the plugin seemed pretty old, so I was wondering if there was a more up-to-date plugin people were using. I did some Googling, and saw a few post explaining how to configure it with Jekyll sites using the Chirpy theme. While this theme does look nice, and maybe I'll check it out someday, I wanted to keep things simple and do things with the Minima 3 setup I'm currently using. I was about to just write my own template to handle this, but then I wondered: is there a chance that this is already builtin to Minima?

Turns out: yep.

## Adding Google Analytics with the Minima theme

After looking at the source code for their default head template, I realized that all I needed to do was add this to my `_config.yml` (at the top level, not nested under the `minima:` section or anything):

```yaml
google_analytics: <my analytics ID>
```

I ran `JEKYLL_ENV=production bundle exec jekyll serve`, and there it was: my Google Analytics tag. Pretty slick!

Now I just gotta wait for the Google Analytics dashboard to start reporting data. In my experience this can take a while, they even say to wait up to 48 hours after deployment. It does seem to have some data and using their test function verified that the site was setup correctly, so now time to exercise patience.
