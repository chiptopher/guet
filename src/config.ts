import { Committer } from './committer';

export interface Config {
    committers: Committer[];
}

export function emptyConfig() {
    return {
        committers: [],
    };
}
