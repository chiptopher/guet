import { ChainLink } from './chain-links';
import { log } from './native-wrapper';

export class Command {
    public readonly identifier: string;
    help: HelpMessage;
    links: ChainLink;
    public readonly printHelpOnNoArgs;

    constructor(
        identifier: string,
        help: HelpMessage,
        links: ChainLink,
        printHelpOnNoArgs = false
    ) {
        this.identifier = identifier;
        this.help = help;
        this.links = links;
        this.printHelpOnNoArgs = printHelpOnNoArgs;
    }

    public execute(args: string[]) {
        if (args.length === 0 && this.printHelpOnNoArgs) {
            log(this.helpMessage('long'));
            process.exit(1);
        }
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
