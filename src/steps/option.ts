import { Step } from './step';
import { Args } from '../args';

export type OptionChooser = (args: Args) => number;

export class OptionStep extends Step {
    private options: Step[];
    private choice: OptionChooser;

    constructor(options: Step[], choice: OptionChooser) {
        super();
        this.options = options;
        this.choice = choice;
    }

    protected doPlay(args: Args): void {
        this.options[this.choice(args)].play(args);
    }
}
