import { ClosureChainLink, Command } from '../command';
import {
    Committer,
    getAvailableCommitters,
    getCurrentCommitters,
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
    getAvailableCommitters()
        .map(mapCommitter)
        .forEach(line => console.log(line));
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
