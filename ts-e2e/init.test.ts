import fs from 'fs';

import colors from 'colors';

import { configPath, readJSONFile } from '../src/utils';
import { assembleOutput, cleanup, run } from './utils';

colors.enable();

describe('guet init', () => {
    beforeEach(() => {
        cleanup();
    });
    it('should create a guet config folder in the root directory', () => {
        run('git init');
        run('guet init');
        expect(fs.existsSync(configPath)).toEqual(true);
    });

    it('tells the user the folder has been successfully created', () => {
        run('git init');
        const [out] = run('guet init');
        const expectedOutput =
            'guet successfully started in this repository.'.green + '\n';
        expect(out).toEqual(expectedOutput);
    });

    it("tells the user when there's no git folder in the given directory", () => {
        run('rm -rf .git');
        const [out] = run('guet init');
        const expectedOutput = assembleOutput([
            'git not installed in this directory.'.red,
        ]);
        expect(out).toEqual(expectedOutput);
    });

    it('writes config boilerplate to config file', () => {
        run('git init');
        run('guet init');

        const found = readJSONFile(configPath);
        expect(found).toEqual({ committers: [] });
    });
});
