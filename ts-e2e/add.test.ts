import colors from 'colors';

import { readJSONFile, configPath } from '../src/utils';
import { assembleOutput, cleanup, run } from './utils';

colors.enable();

describe('guet add', () => {
    beforeEach(() => {
        cleanup();
    });

    it('should add the committer', () => {
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

    describe('when given too many args', () => {
        let out: string;
        let statusCode: number;

        beforeEach(() => {
            run('guet init');
            [out, statusCode] = run(
                'guet add fn "full name" fullname@example.com extra'
            );
        });

        it('should error when too many args have been given', () => {
            expect(out).toEqual(assembleOutput(['Too many arguments.'.red]));
        });

        it('should not add the committer', () => {
            const found = readJSONFile(configPath);
            expect(found.committers).toHaveLength(0);
        });

        it('should report an error code', () => {
            expect(statusCode).toEqual(1);
        });
    });
    describe('when given too many args', () => {
        let out: string;
        let statusCode: number;

        beforeEach(() => {
            run('guet init');
            [out, statusCode] = run(
                'guet add fn "full name" fullname@example.com extra'
            );
        });

        it('should error when too many args have been given', () => {
            expect(out).toEqual(assembleOutput(['Too many arguments.'.red]));
        });

        it('should not add the committer', () => {
            const found = readJSONFile(configPath);
            expect(found.committers).toHaveLength(0);
        });

        it('should report an error code', () => {
            expect(statusCode).toEqual(1);
        });
    });

    describe('when given too few args', () => {
        test.each(['guet add fn', 'guet add fn "full name"'])(
            `too fiew args in "%s"`,
            command => {
                run('guet init');
                const [out, statusCode] = run(command);
                expect(out).toEqual(assembleOutput(['Too few arguments.'.red]));
                const found = readJSONFile(configPath);
                expect(found.committers).toHaveLength(0);
                expect(statusCode).toEqual(1);
            }
        );
    });

    it('should warn user when overwriting user with matching initials', () => {
        run('guet init');
        run('guet add fn "first name1" firstname@example.com');
        const [out, statusCode] = run(
            'guet add fn "first name2" firstname@example.com'
        );

        expect(out).toEqual(
            assembleOutput([
                'Failed to write "fn" "first name2" "firstname@example.com" because it would overwrite already present committer: "fn" "first name1" "firstname@example.com"'
                    .red,
                'You can force this overwrite by adding the --force flag.'.red,
            ])
        );

        expect(statusCode).toEqual(1);
    });

    it('should overwrite the previous user when --force flag is given', () => {
        run('guet init');
        run('guet add fn "first name1" firstname@example.com');
        const [out] = run(
            'guet add fn "first name2" firstname@example.com --force'
        );

        const found = readJSONFile(configPath);
        expect(found.committers).toHaveLength(1);
        expect(found.committers[0]).toEqual({
            email: 'firstname@example.com',
            fullName: 'first name2',
            initials: 'fn',
        });

        expect(out).toEqual(
            assembleOutput([
                'Overwritting previous committer with initials "fn".'.green,
            ])
        );
    });

    xit("should create the config file if it deosn'nt already exist", () => {
        // TODO
    });
});
