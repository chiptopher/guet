import { execSync } from 'child_process';
import fs, { existsSync, PathLike, readFileSync } from 'fs';
import { homedir } from 'os';
import path from 'path';

import { Config, RepoInfo } from './config';

export const configPath = path.join(homedir(), '.guetrc.json');

export function getGitPath() {
    const root = getProjectAbsolutePath();
    if (root) {
        return path.join(root, '.git');
    } else {
        throw new Error('Expected to find a root path, but none was provided');
    }
}

export const COMMIT_EDITMSG = 'COMMIT_EDITMSG';

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

export function repoConfigExists(): boolean {
    return existsSync(path.join(getGitPath(), 'repo.guetrc.json'));
}

export function readRepoConfig(): RepoInfo {
    const projectConfigPath = path.join(getGitPath(), 'repo.guetrc.json');
    const projectConfig = readJSONFile(projectConfigPath);
    return projectConfig;
}

export function writeRepoConfig(data: RepoInfo) {
    const projectConfigPath = path.join(getGitPath(), 'repo.guetrc.json');
    wrtiteJsonFile(projectConfigPath, data);
}

function localConfigFilePath(): string | null {
    const root = getProjectAbsolutePath();
    if (root) {
        return path.join(root, 'guetrc.json');
    } else {
        return null;
    }
}

export function readLocalConfig(): Config | null {
    const path = localConfigFilePath();
    if (path === null) {
        return null;
    } else {
        return readJSONFile(path);
    }
}

export function writeLocalConfig(data: Config) {
    const path = localConfigFilePath();
    if (path) {
        wrtiteJsonFile(path, data);
    }
}

export function localConfigExists(): boolean {
    const path = localConfigFilePath();
    if (!path) return false;
    return existsSync(path);
}

export type Args = string[];

export function getProjectAbsolutePath(): null | string {
    try {
        return String(execSync('git rev-parse --show-toplevel')).trim();
    } catch (e: any) {
        return null;
    }
}
