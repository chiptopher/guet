import { Args } from '../args';

export abstract class Step {
    private _next?: Step;
    constructor() {}

    public next(next: Step): Step {
        this._next = next;
        return this;
    }

    public abstract doPlay(args: Args): void;

    public play(args: Args) {
        this.doPlay(args);
        if (this._next) {
            this._next.play(args);
        }
    }
}
