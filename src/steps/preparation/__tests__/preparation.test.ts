import { Preparation } from '../preparation';
import { Args } from '../../../args';

class MockPreparation extends Preparation {
    public prepare(args: Args) {}
}

describe('Preparation', () => {
    describe('doPlay', () => {
        test('should call prepare', () => {
            const preparation = new MockPreparation();
            preparation.prepare = jest.fn();

            preparation.doPlay({ args: [] });
            expect(preparation.prepare).toHaveBeenCalledWith({ args: [] });
        });
    });
});
