import path from 'path';

import { readJSONFile } from '../src/utils';
import { run } from './utils';

test('when the version flag is given as the command, it prints the current version', () => {
    const [output] = run('guet --version');
    const version = readJSONFile(
        path.join(__dirname, '..', 'package.json')
    ).version;
    expect(output).toEqual(`${version}\n`);
});
