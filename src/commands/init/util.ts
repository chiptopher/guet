export function createGitHookContent(name: string) {
    return `
#!/usr/bin/env sh
set -e
echo "running guet hook ${name}"
npx guet hook ${name}
`;
}
