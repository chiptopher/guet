import { Config } from './config';
import { setGitAuthor } from './git';
import {
    localConfigExists,
    readConfig,
    readLocalConfig,
    readRepoConfig,
    writeConfig,
    writeLocalConfig,
    writeRepoConfig,
} from './utils';

export interface Committer {
    email: string;
    fullName: string;
    initials: string;
}

type ConfigType = 'local' | 'global';

export function removeCommitterWithInitials(
    initials: string,
    type: ConfigType = 'global'
) {
    let globalConfig: Config;

    if (type === 'global') {
        globalConfig = readConfig();
    } else {
        globalConfig = readLocalConfig();
    }

    let committers = [...globalConfig.committers];
    committers = committers.filter(
        committer => committer.initials !== initials
    );

    if (type === 'global') {
        writeConfig({
            ...globalConfig,
            committers,
        });
    } else {
        writeLocalConfig({
            ...globalConfig,
            committers,
        });
    }
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
    const globalCommitters = readConfig().committers;
    let localCommitters: Committer[] = [];
    if (localConfigExists()) {
        localCommitters = readLocalConfig().committers;
    }

    return localCommitters.concat(
        globalCommitters.filter(
            globalCommitter =>
                !localCommitters.find(
                    localCommitter =>
                        globalCommitter.initials === localCommitter.initials
                )
        )
    );
}

export function setCurrentCommitters(committers: Committer[]) {
    writeRepoConfig({
        ...readRepoConfig(),
        currentCommittersInitials: committers.map(c => c.initials),
    });

    setGitAuthor(committers[0]);
}

export function addCommitter(
    _committer: Committer,
    _type?: 'local' | 'global'
) {
    let globalConfig: Config;

    if (_type === undefined || _type === 'global') {
        globalConfig = readConfig();
    } else {
        globalConfig = readLocalConfig();
    }

    const committers = [...globalConfig.committers];
    committers.push(_committer);

    if (_type === undefined || _type === 'global') {
        writeConfig({
            ...globalConfig,
            committers,
        });
    } else {
        writeLocalConfig({
            ...globalConfig,
            committers,
        });
    }
}
