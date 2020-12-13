const { build } = require('gluegun');

async function run(argv) {
    const cli = build()
        .brand('guet')
        .src(__dirname)
        .plugins('./node_modules', { matching: 'guet-*', hidden: true })
        .help()
        .version()
        .create();

    const toolbox = await cli.run(argv);

    return toolbox;
}

module.exports = { run };
