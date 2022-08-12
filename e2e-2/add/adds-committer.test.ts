import { configPath, readJSONFile } from '../../src/utils';
import { run } from '../../ts-e2e/utils';

test('should add the committer', () => {
    run('guet init');
    run('guet add fn "full name" fullname@example.com');

    const found = readJSONFile(configPath);

    expect(found.committers).toEqual([
        {
            email: 'fullname@example.com',
            fullName: 'full name',
            initials: 'fn',
        },
    ]);
});
