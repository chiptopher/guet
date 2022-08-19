jest.mock('./utils');
import {
    addCommitter,
    Committer,
    getAvailableCommitters,
    getCurrentCommitters,
} from './committer';
import { emptyConfig, emptyRepoInfo } from './config';
import {
    readConfig,
    readRepoConfig,
    readLocalConfig,
    localConfigExists,
    writeConfig,
    writeLocalConfig,
} from './utils';

describe('committer.ts', () => {
    beforeEach(() => {
        // @ts-ignore
        readConfig.mockReturnValue(emptyConfig());
        // @ts-ignore
        readRepoConfig.mockReturnValue(emptyRepoInfo());
        // @ts-ignore
        readLocalConfig.mockReturnValue(undefined);

        // @ts-ignore
        localConfigExists.mockReturnValue(false);
    });

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

    describe('getAvailableCommitters', () => {
        it('returns committers in the global config', () => {
            const mockCommitters = [
                {
                    email: 'first@example.com',
                    fullName: 'First',
                    initials: 'f',
                },
            ];

            // @ts-ignore
            readConfig.mockReturnValue({
                committers: mockCommitters,
            });

            expect(getAvailableCommitters()).toEqual(mockCommitters);
        });
        it('overwrites global committers with local committers by the same initials', () => {
            const mockGlobalCommitters = [
                {
                    email: 'first@example.com',
                    fullName: 'First',
                    initials: 'f',
                },
                {
                    email: 'second@example.com',
                    fullName: 'Second',
                    initials: 's',
                },
            ];

            // @ts-ignore
            readConfig.mockReturnValue({
                committers: mockGlobalCommitters,
            });

            // @ts-ignore
            localConfigExists.mockReturnValue(true);

            const mockLocalCommitters = [
                {
                    email: 'sevenths@example.com',
                    fullName: 'Seventh',
                    initials: 's',
                },
            ];

            // @ts-ignore
            readLocalConfig.mockReturnValue({
                committers: mockLocalCommitters,
            });

            expect(getAvailableCommitters()).toEqual([
                mockLocalCommitters[0],
                mockGlobalCommitters[0],
            ]);
        });

        it('includes committers with initials only in local config', () => {
            const mockGlobalCommitters = [
                {
                    email: 'first@example.com',
                    fullName: 'First',
                    initials: 'f',
                },
            ];

            // @ts-ignore
            readConfig.mockReturnValue({
                committers: mockGlobalCommitters,
            });

            const mockLocalCommitters = [
                {
                    email: 'sevenths@example.com',
                    fullName: 'Seventh',
                    initials: 's',
                },
            ];

            // @ts-ignore
            localConfigExists.mockReturnValue(true);

            // @ts-ignore
            readLocalConfig.mockReturnValue({
                committers: mockLocalCommitters,
            });

            expect(getAvailableCommitters()).toEqual([
                mockLocalCommitters[0],
                mockGlobalCommitters[0],
            ]);
        });
    });

    describe('addCommitter', () => {
        it('should add committer to the global config', () => {
            const committer: Committer = {
                email: 'second@example.com',
                fullName: 'Second',
                initials: 's',
            };

            const mockGlobalCommitters = [
                {
                    email: 'first@example.com',
                    fullName: 'First',
                    initials: 'f',
                },
            ];

            // @ts-ignore
            readConfig.mockReturnValue({
                ...emptyConfig(),
                committers: mockGlobalCommitters,
            });

            addCommitter(committer);

            expect(writeConfig).toHaveBeenCalledWith({
                ...emptyConfig(),
                committers: [...mockGlobalCommitters, committer],
            });
        });
    });

    it('should be able to add a committer to the local config', () => {
        const committer: Committer = {
            email: 'second@example.com',
            fullName: 'Second',
            initials: 's',
        };

        const mockLocalConfig = [
            {
                email: 'first@example.com',
                fullName: 'First',
                initials: 'f',
            },
        ];

        // @ts-ignore
        readLocalConfig.mockReturnValue({
            ...emptyConfig(),
            committers: mockLocalConfig,
        });

        addCommitter(committer, 'local');

        expect(writeLocalConfig).toHaveBeenCalledWith({
            ...emptyConfig(),
            committers: [...mockLocalConfig, committer],
        });
    });
});
