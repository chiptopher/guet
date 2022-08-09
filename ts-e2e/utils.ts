import { execSync } from 'child_process';

export function run(command: string) {
    return execSync(command, { encoding: 'utf8' });
}

export function assembleOutput(lines: string[]): string {
    return lines.map(line => line + '\n').join('');
}
