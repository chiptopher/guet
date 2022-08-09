import fs, { PathLike } from 'fs';
import { homedir } from 'os';
import path from 'path';

import colors from 'colors';

import { Config } from '../src/config';
import { assembleOutput, run } from './utils';

colors.enable();

const readJSONFile = (path: PathLike): Config => {
    const rawdata: any = fs.readFileSync(path);
    const student = JSON.parse(rawdata);
    return student;
};

describe('guet init', () => {
    let configPath: string;
    beforeEach(() => {
        configPath = path.join(homedir(), '.guetrc.json');
    });
    it('should create a guet config folder in the root directory', () => {
        run('git init');
        run('guet init');
        expect(fs.existsSync(configPath)).toEqual(true);
    });

    it('tells the user the folder has been successfully created', () => {
        run('git init');
        const out = run('guet init');
        const expectedOutput =
            'guet successfully started in this repository.'.green + '\n';
        expect(out).toEqual(expectedOutput);
    });

    it("tells the user when there's no git folder in the given directory", () => {
        run('rm -rf .git');
        const out = run('guet init');
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
