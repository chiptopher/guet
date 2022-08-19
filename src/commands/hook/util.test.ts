import { DateTime } from 'luxon';

import { Committer } from '../../committer';
import {
    appendCoAuthoredBy,
    shouldResetCommitters,
    shuffleCommitters,
} from './util';

describe('appendCoAuthoredBy', () => {
    it('should add the co-authored-by to the end of a clean commit message', () => {
        const current = 'Initial commit\n';
        const committers: Committer[] = [
            {
                email: 'name@example.com',
                fullName: 'name',
                initials: '',
            },
        ];
        const result = appendCoAuthoredBy(current, committers);

        expect(result).toEqual(
            'Initial commit\n\nCo-authored-by: name <name@example.com>\n'
        );
    });
    it('should replace old Co-authored-by messages with a new one', () => {
        const current = 'Initial commit\n';
        const committers: Committer[] = [
            {
                email: 'name2@example.com',
                fullName: 'name2',
                initials: '',
            },
        ];
        const result = appendCoAuthoredBy(current, committers);

        expect(result).toEqual(
            'Initial commit\n\nCo-authored-by: name2 <name2@example.com>\n'
        );
    });
});

describe('shuffleCommitters', () => {
    it('should make the first committer the last committer', () => {
        const committers: Committer[] = [
            {
                email: 'name1@example.com',
                fullName: 'name1',
                initials: '',
            },
            {
                email: 'name2@example.com',
                fullName: 'name2',
                initials: '',
            },
            {
                email: 'name3@example.com',
                fullName: 'name3',
                initials: '',
            },
        ];

        const result = shuffleCommitters(committers);

        expect(result).toEqual([committers[1], committers[2], committers[0]]);
    });
});

describe('shouldResetCommitters', () => {
    it('should return true if then is over 24 before now', () => {
        const now = DateTime.now();
        const then = now.minus({ hours: 24, seconds: 3 });
        const result = shouldResetCommitters(now, then);
        expect(result).toBe(true);
    });
});
