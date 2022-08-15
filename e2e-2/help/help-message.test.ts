import { run } from '../utils';

test('prints the help message', () => {
    const [outputEmptyArgs] = run('guet');
    const [outputOneDash] = run('guet -h');
    const [outputTwoDash] = run('guet --help');
    const [outputWithInvalidCommand] = run('guet invalid');

    expect(outputEmptyArgs).toContain('usage');
    expect(outputOneDash).toContain('usage');
    expect(outputTwoDash).toContain('usage');
    expect(outputWithInvalidCommand).toContain('usage');
});
