jest.mock('./utils');
import { getCurrentCommitters } from './committer';
import { readConfig, readRepoConfig } from './utils';

readRepoConfig();
describe('getCurrentCommitters', () => {
    it('maintains the order of the committer initials', () => {
        // @ts-ignore
        readRepoConfig.mockReturnValue({
            currentCommittersInitials: ['b', 'a'],
        });

        const mockCommitters = [
            {
                email: 'a@example.com',
                fullName: 'A',
                initials: 'a',
            },
            {
                email: 'b@example.com',
                fullName: 'B',
                initials: 'b',
            },
        ];

        // @ts-ignore
        readConfig.mockReturnValue({
            committers: mockCommitters,
        });

        expect(getCurrentCommitters()).toEqual([
            mockCommitters[1],
            mockCommitters[0],
        ]);
    });
});
