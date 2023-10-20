# move-off-dockerhub

A simple commandline utility to copy many tags (regex filtered) of a docker image from one registry to another

## Why?

When you wanna move off [DockerHub](https://hub.docker.com) to another docker registry
that hasn't kicked you off yet (such as [quay.io](https://quay.io)), you ideally wanna
bring at least *some* of your old images over. This way, if any of your end users are
throttled by DockerHub, you can tell them 'hey just point to the same image on quay.io
instead, and it will continue to work until IBM enshittifies it!'. This small application
lets you copy a subset of tags from your old registry to new by filtering with a regex!

## Installation

You can install this from PyPI:

```bash
pip install move-off-dockerhub
```

You also need [skopeo](https://github.com/containers/skopeo/blob/main/install.md) installed.
Fairly easy, it's packaged well for most distributions / on homebrew.

## Usage

### Login to the docker registries

It's best if you login to both the source and destination docker registries, so you
aren't throttled at the source and have ability to push to the destination. You can
do so with [`skopeo login`](https://github.com/containers/skopeo/blob/main/docs/skopeo-login.1.md).

```bash
# Login to DockerHub
$ skopeo login docker.io
Username: <enter-username>
Password: <enter-password>
Login Succeeded!
$ skopeo login quay.io
Username: <enter-username>
Password: <enter-password>
Login Succeeded!
```

### Do a dry run to figure out which tags to copy

You can now do a dry run to look at the list of tags, and filter out which ones you
wanna copy.

I'm going to use `jupyterhub/k8s-hub` on dockerhub as the example. It gets a tag
pushed for each commit to [zero-to-jupyterhub-on-k8s](https://z2jh.jupyter.org)
that touches the hub. But we only want to copy over the images for the released
versions.

```bash
$ move-off-dockerhub jupyterhub/k8s-hub quay.io/jupyterhub/k8s-hub '.*' --dry-run
<list-of-551-tags>
```

The first argument is the source image, second is the destination (ignored right now),
and the third is a (quoted) regex that tags must match to be copied. The `--dry-run`
shows just the list of tags that would be copied but doesn't actually copy. In this case, we
specify `.*` so we can just look at all the tags, sacrifice a goat to the professor
and construct a regular expression that lists just the tags we want.

After some trial and sacrifice, we find the perfect readable incantation that
gives us all the tags we want

```bash
$ move-off-dockerhub jupyterhub/k8s-hub quay.io/jupyterhub/k8s-hub 'v?\d+\.\d+\.?\d*$' --dry-run
Copying the following tags:
0.10.0
0.10.1
0.10.2
0.10.3
0.10.4
0.10.5
0.10.6
0.11.0
0.11.1
0.7.0
0.8.0
0.8.1
0.8.2
0.9.0
0.9.1
1.0.0
1.0.1
1.1.0
1.1.1
1.1.2
1.1.3
1.1.4
1.2.0
2.0.0
3.0.0
3.0.1
3.0.2
3.0.3
3.1.0
v0.1
v0.3.1
v0.4
v0.5.0
v0.6
```

`v?\d+\.\d+\.\d*$` looks for tags that optionally have a `v` up front (because
some releases did), and then three numbers (of any length) separated by a dot, with
the last number being optional. Making this regex took a lot of sacrifice on behalf
of these electrons, I hope you appreciate them.

### Actually do the copy

First, make sure you have a good internet connection. If you have a friend trying
to watch the cricket worldcup on the same internet connection as you while you do
this, you gonna have a fight. Don't do it.

When the coast is clear, run the same command but without `--dry-run`.

```
$ move-off-dockerhub jupyterhub/k8s-hub quay.io/jupyterhub/k8s-hub 'v?\d+\.\d+\.?\d*$' --dry-run
<lots--of-information-you-don't-need-will-be-output-and-inside-it-will-be-some-info-you-want>
```

Now just wander around, drink some coffee, feed some cats, try to figure out what
you are going to write in the release notes, what the point of venture capital is, etc
as the images copy over.

If your source images are multiarch, all the available architectures will be copied over.

If you run the script again, previously copied tags will still attempt to be copied
but probably go by real quick. `skopeo` is built by some smart people so I just assume
they do something smart and have not actually verified this.

## Why is it called that?

I didn't get enough sleep last night, so my brain could not think of a better name.
NOW YOU ARE STUCK WITH IT HAHA.

If you want this to be a different name, I'm open to suggestions but only from people
who have not posted on Twitter in the last 3 months.

## Why is it AGPL?

As a child, I started writing code that others found useful 'for fun'. As an
adult, I'm very privileged to be able to write code for causes I care about, in
community with people who treat me well, *and* get paid for it! This is awesome!
In therapy, we have discovered it is still quite important to do things
'just for fun'. Writing code that's not actually useful to anyone doesn't feel like 'fun'
to me, but I also wanted to experience the feeling of 'hey, something new!'.

Now, this project was created definitely very much for the benefit of the Jupyter Project.
Given the commandline nature of this project, it should have 0 actual impact on any users. But maybe
the newness of it will give me a dopamine hit!?! We'll find out.
