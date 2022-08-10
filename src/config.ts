import { Committer } from './committer';

export interface Config {
    committers: Committer[];
}

export function emptyConfig() {
    return {
        committers: [],
    };
}

export interface RepoInfo {
    currentCommittersInitials: string[];
}

export function emptyRepoInfo() {
    return {
        currentCommittersInitials: [],
    };
}
