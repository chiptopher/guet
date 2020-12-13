const { system, filesystem } = require('gluegun');

const src = filesystem.path(__dirname, '..');

const cli = async cmd =>
    system.run('node ' + filesystem.path(src, 'bin', 'guet') + ` ${cmd}`);

test('outputs version', async () => {
    const output = await cli('--version');
    expect(output).toContain('3.0.0');
});

test('outputs help', async () => {
    const output = await cli('--help');
    expect(output).toContain('3.0.0');
});
