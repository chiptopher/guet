import { Hook, HookName } from '../hook';
import { filesystem } from 'gluegun';

jest.mock('gluegun');

describe('Hook', () => {
    describe('exists', () => {
        test('should return false if the file does not exist', () => {
            //@ts-ignore
            filesystem.path.mockReturnValue('path/to/.git/hooks/pre-commit');

            //@ts-ignore
            filesystem.exists.mockReturnValue(false);

            const hook = new Hook('path/to/.git', HookName.PreCommit);
            expect(hook.exists()).toBe(false);
        });

        test('should return true if the path exists', () => {
            const expectedPath = 'path/to/.git/hooks/pre-commit';
            //@ts-ignore
            filesystem.path.mockReturnValue('path/to/.git/hooks/pre-commit');

            //@ts-ignore
            filesystem.exists.mockImplementation((path: string) => {
                return path === expectedPath;
            });

            const hook = new Hook('path/to/.git', HookName.PreCommit);
            expect(hook.exists()).toBe(false);
        });
    });
});
