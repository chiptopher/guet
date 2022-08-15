import { setGitAuthor } from './git';
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
    const allCommitters = getAvailableCommitters();

    return currentComitterInitials.map(initials => {
        const found = allCommitters.find(
            committer => committer.initials === initials
        );
        if (!found) {
            // TODO implement
            throw new Error('Unexpected');
        }
        return found;
    });
}

export function getAvailableCommitters(): Committer[] {
    return readConfig().committers;
}

export function setCurrentCommitters(committers: Committer[]) {
    writeRepoConfig({
        ...readRepoConfig(),
        currentCommittersInitials: committers.map(c => c.initials),
    });

    setGitAuthor(committers[0]);
}
