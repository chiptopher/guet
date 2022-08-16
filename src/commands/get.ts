import { ClosureChainLink, Command } from '../command';
import {
    Committer,
    getCurrentCommitters,
    getGlobalCommitters,
    getLocalCommitters,
} from '../committer';

function getCommitters(args: string[]) {
    const [which] = args;
    switch (which) {
        case 'current':
            return currentCommitters();
        case 'all':
            return allCommitters();
    }
}

function currentCommitters() {
    console.log('Current committers:');
    getCurrentCommitters()
        .map(mapCommitter)
        .forEach(line => console.log(line));
}

function allCommitters() {
    console.log('All committers:');
    const globalCommitters = getGlobalCommitters();
    const localCommitters = getLocalCommitters();

    globalCommitters
        .map(committer => {
            if (
                localCommitters.find(
                    localCommiter =>
                        localCommiter.initials === committer.initials
                )
            ) {
                return `${mapCommitter(committer)} (overriden)`;
            } else {
                return mapCommitter(committer);
            }
        })
        .forEach(line => console.log(line));

    if (localCommitters.length > 0) {
        console.log('\n(local)');
        localCommitters.map(mapCommitter).forEach(line => console.log(line));
    }
}

function mapCommitter({ email, fullName, initials }: Committer) {
    return `${initials} - ${fullName} <${email}>`;
}

export const getCommand = new Command(
    'get',
    {
        description: 'Get information about the available committers.',
        usage: `usage: guet get <identifier>
    current - lists currently set comitters
    all - lists all committers`,
    },
    new ClosureChainLink(getCommitters)
);
