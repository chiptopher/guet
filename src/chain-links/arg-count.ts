import { ChainLink } from '.';
import { separateFlags } from '../args';

export class ArgCount extends ChainLink {
    private min: number;
    private max: number;

    constructor(min: number, max: number) {
        super();
        this.min = min;
        this.max = max;
    }

    protected doExecute(args: string[]): void {
        const [withoutFlags] = separateFlags(args);
        if (withoutFlags.length < this.min) {
            console.log('Too few arguments.'.red);
            process.exit(1);
        } else if (withoutFlags.length > this.max) {
            console.log('Too many arguments.'.red);
            process.exit(1);
        }
    }
}
