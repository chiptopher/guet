# Frequently Asked Questions

### How do I use guet with [husky](https://github.com/typicode/husky)?

To use guet with husky, you will need to start guet tracking alongside any present git hooks. To accomplish this, use the commmand `guet start -a`. guet uses the pre-commit, post-commit, and commit-msg hooks, so you'll need to update them in husky to look something like this:
```json
  "husky": {
    "hooks": {
      "pre-commit": "yarn test && .git/hooks/pre-commit-guet",
      "commit-msg": "yarn test && .git/hooks/commit-msg-guet",
      "post-commit": "yarn test && .git/hooks/post-commit-guet"
    }
  }
```

