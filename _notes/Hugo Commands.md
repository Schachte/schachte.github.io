# Hugo Commands

Installing hugo

```bash
brew install hugo
```

New site

```bash
hugo new site mysite
```

Building the code

```bash
hugo server -t your-theme
```

Viewing the site locally

```bash
hugo server
```

Adding submodule to public directory

- Make sure you have at least one commit on the `main` branch on the target repo before running this

```bash
git submodule add -b main YOUR_REPO_URL.git public
```

Creating a deployment script

```bash
#!/bin/sh

# If a command fails then the deploy stops
set -e

printf "\033[0;32mDeploying updates to GitHub...\033[0m\n"

# Build the project.
hugo # if using a theme, replace with `hugo -t <YOURTHEME>`

# Go To Public folder
cd public

# Add changes to git.
git add .

# Commit changes.
msg="rebuilding site $(date)"
if [ -n "$*" ]; then
	msg="$*"
fi
git commit -m "$msg"

# Push source and build repos.
git push origin main
```