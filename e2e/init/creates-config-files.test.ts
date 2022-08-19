import fs from 'fs';
import path from 'path';

import colors from 'colors';

import { configPath, getGitPath, readJSONFile } from '../../src/utils';
import { run } from '../utils';

colors.enable();

test('creates config files', () => {
    run('git init');
    const [out, exitCode] = run('guet init');

    expect(fs.existsSync(configPath)).toEqual(true);
    expect(exitCode).toEqual(0);

    const expectedOutput =
        'guet successfully started in this repository.'.green + '\n';
    expect(out).toEqual(expectedOutput);

    const found = readJSONFile(configPath);
    expect(found).toEqual({ committers: [] });

    expect(fs.existsSync(path.join(getGitPath(), 'repo.guetrc.json'))).toEqual(
        true
    );
});
