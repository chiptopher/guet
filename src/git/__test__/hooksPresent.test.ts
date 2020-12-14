import { projectRoot } from '../../util/projectRoot';
import { NoProjectRootError } from '../../errors';
import { hooksPresent } from '../hooksPresent';
import { filesystem } from 'gluegun';

jest.mock('../../util/projectRoot');
jest.mock('gluegun');

describe('hooksPresent', () => {
    beforeEach(() => {
        jest.resetAllMocks();
    });

    test('should return false if no root project is found', () => {
        //@ts-ignore
        projectRoot.mockImplementation(() => {
            throw new NoProjectRootError();
        });

        expect(hooksPresent()).toBe(false);
    });

    test('should return true if files exist', () => {
        //@ts-ignore
        projectRoot.mockReturnValue('/path/to/project/root');

        //@ts-ignore
        filesystem.exists.mockReturnValue(true)

        expect(hooksPresent()).toBe(true);

        const commitMsgPath = filesystem.path(
            filesystem.path(filesystem.cwd(), '.git'),
            'commit-msg'
        );
        const preCommit = filesystem.path(
            filesystem.path(filesystem.cwd(), '.git'),
            'commit-msg'
        );
        const postCommit = filesystem.path(
            filesystem.path(filesystem.cwd(), '.git'),
            'commit-msg'
        );

        expect(filesystem.exists).toHaveBeenCalledWith(commitMsgPath);
        expect(filesystem.exists).toHaveBeenCalledWith(preCommit);
        expect(filesystem.exists).toHaveBeenCalledWith(postCommit);
    });
});
