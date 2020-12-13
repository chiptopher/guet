import { Step } from '../step';
import { Args } from '../../args';
import { print } from 'gluegun';

export abstract class Check extends Step {
    private stopMessage?: string;
    constructor(stopMessage: string) {
        super();
        this.stopMessage = stopMessage;
    }

    public doPlay(args: Args): void {
        if (this.shouldStop(args)) {
            this.printErrorMessage(args);
            process.exit(1);
        }
    }

    private printErrorMessage(args: Args) {
        this.stopMessage
            ? print.info(this.stopMessage)
            : print.info(this.stopMessageHook(args));
    }

    public abstract shouldStop(args: Args): boolean;

    public stopMessageHook(args: Args): string {
        return '';
    }
}
