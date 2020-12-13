import { Check } from '../check';
import { Args } from '../../../args';
import { print } from 'gluegun';

jest.mock('gluegun');

//@ts-ignore
process.exit = jest.fn();

class MockCheck extends Check {
    private result: boolean;

    constructor(result: boolean, message?: string) {
        super(message);
        this.result = result;
    }

    public shouldStop(args: Args): boolean {
        return this.result;
    }

    public stopMessageHook(args: Args): string {
        return 'message';
    }
}

describe('Check', () => {
    describe('doPlay', () => {
        test('should exit if shouldStop returns true', () => {
            const check = new MockCheck(true);
            check.doPlay({ args: [] });
            expect(process.exit).toHaveBeenCalledWith(1);
        });

        test('should print error message', () => {
            const check = new MockCheck(true, 'message');
            check.doPlay({ args: [] });
            expect(print.info).toHaveBeenCalledWith('message');
        });

        test('should use stopMessageHook when no default message provided', () => {
            const check = new MockCheck(true);
            check.doPlay({ args: [] });
            expect(print.info).toHaveBeenCalledWith('message');
        });
    });
});
