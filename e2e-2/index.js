/* eslint-disable @typescript-eslint/no-var-requires */
const { execSync } = require('child_process');

const Docker = require('dockerode');

const output = execSync(`npx jest e2e-2 --listTests`);

async function main() {
    let failed = false;

    const testFiles = String(output)
        .split('\n')
        .filter(line => line !== '');

    for (let i = 0; i < testFiles.length; i++) {
        const testClient = new Docker();
        const runCommand = ['npx', 'jest', testFiles[i].split('guet/')[1]];
        const result = await testClient.run(
            'guettest:0.0.1',
            runCommand,
            process.stdout
        );

        const exitCode = result[0]['StatusCode'];
        if (exitCode > 0) {
            failed = true;
        }
    }

    if (failed) {
        process.exit(1);
    }
}

main().catch(console.error);
