import { Check } from "./check";
import { Args } from "../../args";

export class StartRequiredCheck extends Check {
    public shouldStop(args: Args): boolean {
        throw new Error("Method not implemented.");
    }
}
