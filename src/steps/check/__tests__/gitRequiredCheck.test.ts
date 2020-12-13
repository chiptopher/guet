import { GitRequiredCheck } from '../gitRequiredCheck';
import { filesystem } from 'gluegun';

jest.mock('gluegun');

describe('GitRequiredCheck', () => {
    describe('shouldStop', () => {
        test('should check current directory for git folder', () => {
            const mockExists = jest.fn();
            filesystem.exists = mockExists;
            mockExists.mockReturnValue('dir');

            const check = new GitRequiredCheck();

            expect(check.shouldStop({ args: [] })).toBe(true);
            expect(filesystem.exists).toHaveBeenCalledWith(
                filesystem.path(filesystem.cwd(), '.git')
            );
        });
    });
});
