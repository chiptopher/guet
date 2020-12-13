import { Step } from '../step';
import { Args } from '../../args';

export abstract class Preparation extends Step {
    public doPlay(args: Args) {
        this.prepare(args);
    }

    public abstract prepare(args: Args);
}
