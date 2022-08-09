import fs from 'fs';
import path from 'path';

export function hasGitInCwd() {
    const gitDir = path.join(process.cwd(), '.git');
    return fs.existsSync(gitDir);
}
