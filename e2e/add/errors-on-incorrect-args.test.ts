import colors from 'colors';

import { configPath, readJSONFile } from '../../src/utils';
import { run, assembleOutput } from '../utils';

colors.enable();

test('should fail to add committers when given incorrect args', () => {
    run('guet init');
    let [out, statusCode] = run(
        'guet add fn "full name" fullname@example.com extra'
    );
    expect(out).toEqual(assembleOutput(['Too many arguments.'.red]));
    let found = readJSONFile(configPath);
    expect(found.committers).toHaveLength(0);
    expect(statusCode).toEqual(1);

    [out, statusCode] = run(
        'guet add fn "full name" fullname@example.com extra'
    );
    expect(out).toEqual(assembleOutput(['Too many arguments.'.red]));
    found = readJSONFile(configPath);
    expect(found.committers).toHaveLength(0);
    expect(statusCode).toEqual(1);
});
