import fs, { existsSync, PathLike, readFileSync } from 'fs';
import { homedir } from 'os';
import path from 'path';

import { Config, RepoInfo } from './config';

export const configPath = path.join(homedir(), '.guetrc.json');

export function getGitPath() {
    return path.join(process.cwd(), '.git');
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

const localConfigFilePath = path.join(process.cwd(), 'guetrc.json');

export function readLocalConfig(): Config {
    const projectConfig = readJSONFile(localConfigFilePath);
    return projectConfig;
}

export function writeLocalConfig(data: Config) {
    wrtiteJsonFile(localConfigFilePath, data);
}

export function localConfigExists(): boolean {
    return existsSync(localConfigFilePath);
}

export type Args = string[];
