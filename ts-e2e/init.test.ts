import fs from 'fs';
import path from 'path';

import colors from 'colors';

import { configPath, getGitPath, readJSONFile } from '../src/utils';
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

    it('writes repo config boilerplate into .git/repo.guetrc.json', () => {
        run('git init');
        run('guet init');

        expect(
            fs.existsSync(path.join(getGitPath(), 'repo.guetrc.json'))
        ).toEqual(true);
    });

    describe('when given the --withHooks flag', () => {
        it('should add pre-commit, commit-msg, and post-commit files', () => {
            run('git init');
            run('guet init --withHooks');
            expect(
                fs.existsSync(path.join(getGitPath(), 'hooks', 'pre-commit'))
            ).toEqual(true);
            expect(
                fs.existsSync(path.join(getGitPath(), 'hooks', 'commit-msg'))
            ).toEqual(true);
            expect(
                fs.existsSync(path.join(getGitPath(), 'hooks', 'post-commit'))
            ).toEqual(true);
        });
        it('should put the apropriate content in each file', () => {
            run('git init');
            run('guet init --withHooks');

            const preCommitContent = fs.readFileSync(
                path.join(getGitPath(), 'hooks', 'pre-commit')
            );
            expect(String(preCommitContent)).toEqual(
                '#!/usr/bin/env sh\nnpx guet hook pre-commit\n'
            );

            const postCommitContent = fs.readFileSync(
                path.join(getGitPath(), 'hooks', 'post-commit')
            );
            expect(String(postCommitContent)).toEqual(
                '#!/usr/bin/env sh\nnpx guet hook post-commit\n'
            );

            const commitMsgContent = fs.readFileSync(
                path.join(getGitPath(), 'hooks', 'commit-msg')
            );
            expect(String(commitMsgContent)).toEqual(
                '#!/usr/bin/env sh\nnpx guet hook commit-msg\n'
            );
        });
    });
});
