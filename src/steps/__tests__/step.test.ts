import { Step } from '../step';
import { Args } from '../../args';

export class MockStep extends Step {
    doPlayCalled: boolean;

    constructor() {
        super();
        this.doPlayCalled = false;
    }

    protected doPlay(args: Args) {
        this.doPlayCalled = true;
    }
}

describe('step', () => {
    describe('play', () => {
        test('should play sublcass', () => {
            const step = new MockStep();
            step.play({ args: [] });
            expect(step.doPlayCalled).toBeTruthy();
        });

        test('should call next play if next present', () => {
            const next = new MockStep();
            const step = new MockStep().next(next);
            step.play({ args: [] });

            expect(next.doPlayCalled).toBe(true);
        });
    });

    describe('next', () => {
        test('should return self', () => {
            const step = new MockStep();
            const next = new MockStep();

            expect(step.next(next)).toBe(step);
        });
    });
});
