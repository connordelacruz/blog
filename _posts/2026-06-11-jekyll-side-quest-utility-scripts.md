---
title: "Jekyll Side Quest: Utility Scripts"
tags: jekyll python
---

After getting the basics setup on this Jekyll blog, I decided it might be a good time to throw together some utility scripts to streamline the process of making posts for this blog (and I was looking for an excuse to write some Python). There were two fundamental tasks in particular that I thought could benefit from a little automation:

1. Creating a new post
2. Copying over and organizing images

On paper, those sound like really trivial things, but I think there's more tedium in these tasks than it sounds, and these are things that I expect to do over and over if I'm using this blog.

Additionally, I wanted to setup a top-level script that can execute any of these other scripts as subcommands. So here's what I ended up with:


## Top Level: Single entrypoint for running scripts

I won't get too into the architecture of this here as it's not super interesting, but basically I created `exec_script.py` at the root of this blog's repo, which builds an argument parser for running subcommands from the `scripts/` directory. 

Running it without arguments is equivalent to the `--help` argument, which will list available subcommands:

```
$ ./exec_script.py
usage: exec_script.py [-h] <script> ...

options:
  -h, --help    show this help message and exit

Scripts:
  Run "exec_script.py <script> --help" for details

  <script>
    new-post    Create a new post and open it in editor
    copy-image  Copy image into assets/images/<year>/<month>/<day>/
```

The syntax for running a script is:

```
./exec_script.py <subcommand> [<arguments>]
```

## Script 1: new-post

### Overview

The goal of the first script was to do the following:

- Take the title of a new post I want to write
- sanitize and format the title, join it with the current date to create a filename using Jekyll's post conventions, i.e. `YYYY-MM-DD-lowercase-hyphenated-title-text.md`
- Create the markdown file for the post in the `_posts/` directory
- Put default front matter at the top of the file, followed by a blank line
- Open the new file in Neovim, move the cursor below the front matter, and enter insert mode so I can immediately start writing

Additionally, I wanted to add a couple quality of life features:

- An optional `--date` argument to use a post date other than the current date
- Let me type the title argument without quotes
- If the title I provide has special characters that get stripped when formatting the filename, add the `title` variable to the generated front matter

### Final Product

Source code for the this script can be found [here](https://github.com/connordelacruz/blog/tree/master/scripts/new_post.py).

**Example Usage:**

![Screen recording using the new-post script](/blog/assets/images/2026/06/11/new-post-showcase.gif)

By default, the date stamp for the new file will be the current date. This can be overridden with the `--date` argument:

```
./exec_script.py new-post 'Gotta go back in time' --date 1969-04-20
```

The generated filename in the above example would be `_posts/1969-04-20-gotta-go-back-in-time.md`

While writing this, I realized that double quotes `"` would need to be escaped for the `title` front matter variable. I've implemented this, so running something like:

```
./exec_script.py new-post 'Title with "Double Quotes"'
```

will now correctly escape the quotes. Here's what the resulting front matter from the above looks like:

```yaml
---
title: "Title with \"Double Quotes\""
---
```


## Script 2: copy-image

### Overview

I did some research to see how other folks are organizing their image assets for posts, and the structure I landed on was putting them in subdirectories of `assets/images/` organized by year, month, and day, where the date corresponds to the date of the post the image is used for. E.g. `assets/images/2026/06/11/`. This seemed like a good way to keep track of what images correspond to which posts, granular enough that it's not a big mess, and kept separate from the `_posts/` directory. 

But that's a lot of nested directories, and I feel like doing that manually all the time could get annoying. So my goal for this script was:

- Take the path to the image file I want to use
- Using the current date by default, create any subdirectories of `assets/images/` if necessary for `YYYY/MM/DD/`
- Copy the target image file to the target directory
- Print out the relative path of the copied file so I can copy and paste it into the post

Bonus QOL features:

- An optional `--date` argument to use a post date other than the current date
- An optional `--filename` argument to set a custom name for the copied file (that will also append the correct file extension if it's missing from the argument)

### Final Product

Source code for this script can be found [here](https://github.com/connordelacruz/blog/tree/master/scripts/copy_image_for_post.py).

**Example Usage:**

![Screen recording using the new-post script](/blog/assets/images/2026/06/11/copy-image-showcase.gif)

By default, the filename of the copied file remains the same, but it can be modified with the `--filename` argument:

```
./exec_script.py copy-image ~/Downloads/original-fname.jpg --filename new-fname.jpg
```

The resulting image file with the above example will have the filename `new-fname.jpg`.

Using the `--filename` argument does not require a file extension. Part of the validation ensures that the copied file will always maintain the same extension as the original file. Because of this, the following examples will also create a file called `new-fname.jpg`:

```
./exec_script.py copy-image ~/Downloads/original-fname.jpg --filename new-fname

./exec_script.py copy-image ~/Downloads/original-fname.jpg --filename new-fname.bad-ext
```

**Note:** _Because of how my blog is configured, image paths need to be prefixed with `/blog/` for Jekyll to find them. Right now this script just tacks that on the front, but the obsessive compulsive in me kinda wants to update this to pull the value of `baseurl` from `_config.yml` to make this more dynamic._

### Future Plans

- Optimize copied image for web as part of this script (compress, scale down if it's a larger resolution than necessary)


## Conclusion

I don't know how to end this post lol. I just wanted an excuse to write some Python and make writing posts a little more streamlined, and then use that as an excuse to write a blog post.
