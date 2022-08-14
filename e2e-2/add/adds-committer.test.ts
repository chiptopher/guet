import { configPath, readJSONFile } from '../../src/utils';
import { run } from '../utils';

test('should add the committer', () => {
    run('guet init');
    run('guet add FN "full name" fullname@example.com');

    const found = readJSONFile(configPath);

    expect(found.committers).toEqual([
        {
            email: 'fullname@example.com',
            fullName: 'full name',
            // thier initials should be lowercased when added
            initials: 'fn',
        },
    ]);
});
