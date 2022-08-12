import { readConfig, readRepoConfig, writeRepoConfig } from './utils';

export interface Committer {
    email: string;
    fullName: string;
    initials: string;
}

export function removeCommitterWithInitials(
    initials: string,
    committers: Committer[]
) {
    return committers.filter(committer => committer.initials !== initials);
}

export function getCurrentCommitters(): Committer[] {
    const currentComitterInitials = readRepoConfig().currentCommittersInitials;
    return getAvailableCommitters().filter(committer =>
        currentComitterInitials.includes(committer.initials)
    );
}

export function getAvailableCommitters(): Committer[] {
    return readConfig().committers;
}

export function setCurrentCommitters(committers: Committer[]) {
    writeRepoConfig({
        ...readRepoConfig(),
        currentCommittersInitials: committers.map(c => c.initials),
    });
}
