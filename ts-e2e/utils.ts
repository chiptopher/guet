import { execSync } from 'child_process';
import fs from 'fs';

import { configPath, getGitPath } from '../src/utils';

export function run(command: string): [string, number] {
    try {
        const output = execSync(command, { encoding: 'utf8' });
        return [output, 0];
    } catch (e: any) {
        return [String(e.stdout), 1];
    }
}

export function assembleOutput(lines: string[]): string {
    return lines.map(line => line + '\n').join('');
}

export function cleanup() {
    if (fs.existsSync(configPath)) {
        fs.rmSync(configPath);
    }

    if (fs.existsSync(getGitPath())) {
        run(`rm -rf ${getGitPath()}`);
    }
}
