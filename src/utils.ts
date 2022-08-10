import fs, { PathLike, readFileSync } from 'fs';
import { homedir } from 'os';
import path from 'path';

import { Config } from './config';

export const configPath = path.join(homedir(), '.guetrc.json');

export function getGitPath() {
    return path.join(process.cwd(), '.git');
}

export function hasGitInCwd() {
    const gitDir = path.join(process.cwd(), '.git');
    return fs.existsSync(gitDir);
}

export function readConfig(): Config {
    return readJSONFile(configPath);
}

export function writeConfig(config: Config) {
    wrtiteJsonFile(configPath, config);
}

export function readJSONFile<T = any>(path: PathLike): T {
    const rawdata: any = readFileSync(path);
    const student = JSON.parse(rawdata);
    return student;
}

export function wrtiteJsonFile(path: PathLike, data: any) {
    fs.writeFileSync(path, JSON.stringify(data));
}
