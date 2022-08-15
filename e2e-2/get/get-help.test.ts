import { getHelpText } from '../../src/commands/get';
import { run } from '../utils';

test('prints the help message when no args are provided or the help flag is provided', () => {
    run('git init');
    run('guet init');
    const [noArgsOutput] = run('guet get');
    expect(noArgsOutput).toEqual(getHelpText + '\n');
    const [helpFlagOutput] = run('guet get --help');
    expect(helpFlagOutput).toEqual(getHelpText + '\n');
});
