import { ChainLink } from './chain-links';

export class Command {
    public identifier: string;
    help: HelpMessage;
    links: ChainLink;

    constructor(identifier: string, help: HelpMessage, links: ChainLink) {
        this.identifier = identifier;
        this.help = help;
        this.links = links;
    }

    public execute(args: string[]) {
        this.links.execute(args);
    }

    public helpMessage(size: 'short' | 'long'): string {
        switch (size) {
            case 'short':
                return this.help.description;
            case 'long':
                return `${this.help.description}\nusage: ${this.help.usage}`;
        }
    }
}

interface HelpMessage {
    description: string;
    usage: string;
}

export class ClosureChainLink extends ChainLink {
    private closure: (args: string[]) => void;

    constructor(closure: (args: string[]) => void) {
        super();
        this.closure = closure;
    }

    protected doExecute(args: string[]): void {
        this.closure(args);
    }
}
