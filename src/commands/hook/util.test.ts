import { Committer } from '../../committer';
import { appendCoAuthoredBy } from './util';

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
