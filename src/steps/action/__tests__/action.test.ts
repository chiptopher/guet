import { Action } from '../action';
import { Args } from '../../../args';

class MockAction extends Action {
    public execute(args: Args) {}
}

describe('Action', () => {
    describe('doPlay', () => {
        test('should call execute with given arguments', () => {
            const action = new MockAction();
            action.execute = jest.fn();

            action.doPlay({ args: [] });
            expect(action.execute).toHaveBeenCalledWith({ args: [] });
        });
    });
});
