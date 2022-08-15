export abstract class ChainLink {
    following?: ChainLink;

    execute(args: string[]) {
        this.doExecute(args);
    }

    public next(link: ChainLink) {
        this.following = link;
        return this.following;
    }

    protected abstract doExecute(args: string[]): void;
}

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
}

interface HelpMessage {
    long: string;
    short: string;
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
