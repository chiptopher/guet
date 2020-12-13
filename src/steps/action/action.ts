import { Step } from "../step";
import { Args } from "../../args";

export abstract class Action extends Step {
    public doPlay(args: Args): void {
        this.execute(args);
    }

    public abstract execute(args: Args);
}
