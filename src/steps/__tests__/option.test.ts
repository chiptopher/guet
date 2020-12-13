import { Args } from '../../args';
import { OptionStep } from '../option';
import { Step } from '../step';
import { MockStep } from './step.test';

describe('OptionStep', () => {
    describe('doPlay', () => {
        test('should return', () => {
            const first = new MockStep();
            const second = new MockStep();
            const options: Step[] = [first, second];
            const choice: (args: Args) => number = _ => {
                return 1;
            };
            const step = new OptionStep(options, choice);
            step.play({ args: [] });

            expect(second.doPlayCalled).toBe(true);
        });
    });
});
