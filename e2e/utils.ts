import { execSync } from 'child_process';
import fs from 'fs';

import { configPath, getGitPath } from '../src/utils';

export function run(command: string, cwd?: string): [string, number] {
    try {
        const output = execSync(command, { cwd, encoding: 'utf8' });
        return [String(output), 0];
    } catch (e: any) {
        let output = '';
        if (e.stdout) {
            output = e.stdout;
        } else if (e.stderr) {
            output = e.stderr;
        }
        return [String(output), 1];
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

    run('rm test-*');
}

export function testFileName(name: string) {
    return `test-${name}`;
}
