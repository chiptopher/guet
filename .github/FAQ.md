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

If package.json is not in the root of the repository you'll have to change to the root directory before each guet hook:
```json
  "pre-commit": "yarn test && cd .. && .git/hooks/pre-commit-guet"
```
This will not work: `"post-commit": "../.git/hooks/pre-commit-guet"`

### I want to squash my commit, but still save co-authors. What do I do?

As long as your your `Co-authored-by Name <emai>` lines are in the squashed commit, they will show up. In this example, you can remove all the duplicated lines under the "File 2" commit.

![Squash Commit Example](./images/squashed_commit_example.png)

### What do I need to do to uninstall guet?

`pip3 uninstall guet` is the command you need to run to remove guet. If you're sure that you'll never want to use guet again, you can also remove `~/.guet/`. Additionally, you will need to remove guet from any repositories that you've run `guet start` in. You can do this by removing `pre-commit`, `post-commit`, and `commit-msg` in that repository's `.git/hooks/` folder.
