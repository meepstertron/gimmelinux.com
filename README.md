
# GIMME MY LINUX!

**Stuck in a TryHackMe or CTF challenge and need a Linux box *right now*?**
You're on Windows or macOS and can't be bothered with WSL or setting up a VM?
No worries — we've got you covered.

-> Just open [**gimmelinux.com**](https://gimmelinux.com) in your browser and **boom**:
A **free, no-login Alpine Linux container** is yours to use.

Perfect for:

* Running Linux commands instantly
* Installing obscure Linux-only tools
* Hacking away without any setup
* Messing around in a terminal just for fun

---

## FAQ

### Is it free?

**Yes!** Totally free. No account, no signup, no catch.

### What OS is it running?

We're using [**Alpine Linux**](https://alpinelinux.org/), a super lightweight distro — boots fast, uses minimal resources, and still packs a punch.

### Do I need to log in?

Nope! Just click the link and you’re in. We don’t want your email. We don’t even ask your name.

### What can I do with it?

✅ YES:

* Run tools and scripts
* Use it as a temporary dev environment
* Explore and learn Linux commands
* Test out malware in a safe container
* Install packages with `apk`

🚫 NO:

* Anything illegal (duh)
* Persistent storage (containers are wiped after inactivity)
* Hosting servers or services long-term

### How long does my session last?

Sessions are ephemeral. If you’re inactive for a while or close the tab, it’ll go poof. But hey, just open a new one.

### Can I install software?

Yes! Use Alpine’s `apk` package manager:

```sh
apk update
apk add curl python3 git ...
```

---

## Why use it?

* Zero setup
* Minimal distractions
* Blazingly fast startup
* Great for debugging, testing, and learning
* Works from *any* device with a browser

---

## Contribute

Got a cool idea?
Spotted a bug?
Wanna help make it better?

PRs and issues welcome right here on GitHub
