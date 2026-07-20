---
tags: ipod repair vintage-tech
---

I love old tech. It's always satisfying to find some old device from the pre-enshitification era and get it up and running again. Unfortunately, everything has to be a collectible these days, so finding new nuggets to refurbish can be prohibitively expensive. But I've got the itch, and so the other day when the air was full of hazardous smoke from Canadian wildfires, I figured a good indoor activity would be to see what I've got sitting around that I could work on.

## iPod Mini Backstory

About a year or so back, I stumbled upon an iPod Mini at the thrifts for only $8. This was definitely a fluke, as it was sitting in a bin with a dozen crappy bootleg iPods with price tags 3x higher than the real thing. Maybe it's because the iPod Mini is the odd, forgotten middle child between the Classic and the Nano, and something about its girth made it look less legit than the plastic copycat shuffles with full sized USB ports on them. Anyway, I jumped on the deal, and took my first steps into the iPod modding scene. I got a new battery and a CF to SD card adapter, and before I knew it I had a high-capacity working iPod up and running!

Later that year, a friend of mine gave me a 7th gen iPod Classic he had sitting around. It was a huge pain, but I was able to open that bad boy up and kit it out with a big ass battery and a few hundred gigs of SD card storage. With its slim form factor, nearly infinite battery life, and much improved software, this 7th gen became my daily driver, and the iPod Mini became my fallback player for things like going to the beach.

As the beach season ended and the harsh Chicago winter rolled in, this iPod Mini sat around for many months. When I finally dug it out again and plugged it in, absolutely nothing happened. Since I didn't really need it, I set it aside in the pile of "I'll get to it eventually" projects. And so I guess today is eventually!

## Troubleshooting

My first instinct was to try and clean out any lint from the charging port. I had already tried this in the past, but figured I'd be thorough. I didn't see anything inside, and using a toothpick to gently pick at it yielded no results.

So, annoyingly, that meant the next step was to open it up. I don't like opening this kind of iPod too often if I can avoid it. Getting access to its guts means prying off the top and bottom plastic covers, which have become very brittle over 20+ years, and are mostly held on with adhesive, none of which lends itself to repeat repairs. But thankfully the process is straightforward enough otherwise. I didn't bother taking pictures or anything, but if you're interested on how to get into one of these bad boys, [iFixit has great instructions here](https://www.ifixit.com/Guide/iPod+Mini+Battery+Replacement/411).

Once I had the guts out of the shell, I took a closer look at it, and... I found lint in the charger. My instinct was right all along. It was really packed tight in there, I had to push it out from the holes on the side of the port. So at the very least it wasn't a waste of time opening this up.

After removing the lint, I plugged in a charger, and this time I could hear a weird faint beeping sound coming from it. Kinda scary, but at least it was something different! After doing some googling, I eventually found a Reddit thread of someone with a similar issue, and found [this comment from the OP](https://www.reddit.com/r/ipod/comments/1ek1155/comment/mncbfxz/):

> Seems to be the SD adapter, I had the old hard drive, today I tried installing the original HD and the iPod at least showed a screen saying that need to charge it. Right now I am charging it as it showed a “battery very low “ message. Seems like the SD adapter is somehow preventing the iPod to boot. I suspect that I cannot allow the iPod to get to 0% dead battery, it cannot recover from that. I will write if it was possible to recover it, at least the logic board is ok, I was afraid it might be dead. Edit: It’s alive. It booted from the old HD. I will charge the battery and see if I can install the SD adapter again.
>
> Edit2: It is recovering, seems like it actually cannot recover if the battery is completely drained while using the SD adapter. I recharged the battery with the HDD and then replaced it with the SD and it is working again 😮‍💨

This turned out to be EXACTLY the issue I was having. I dug out the old hard drive that the iPod Mini came with, swapped out the SD card adapter for it, and plugged it in. And this time, it booted!

![iPod Surgery](/blog/assets/images/2026/07/17/ipod-mini-surgery.jpg)

I let it charge for a few hours, then yoinked out the battery (since as far as I know that's the only way to shut down the mini), put the SD card adapter back in, and put it all back together.

![iPod Fixed](/blog/assets/images/2026/07/17/ipod-mini-fixed.jpg)

## Takeaways

This was a fairly simple repair overall, but a nice way to get back into the hobby. My takeaways after wrapping this up:

1. If the charging port stops working, it's probably lint
2. If you can't pick out any lint, it's probably still lint
3. It's good to hoard parts from old projects, even if you think you won't ever need them
4. Reddit kinda sucks, but the niche communities can be great resources for stuff like this

This was kinda fun doing a post-mortem on a little project, so maybe I'll do more posts like this in the future. Honestly, I don't expect there to be an audience for this blog, but maybe something in here will prove useful to someone else.
