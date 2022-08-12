/* eslint-disable @typescript-eslint/no-var-requires */
const { execSync } = require('child_process');

const Docker = require('dockerode');

const output = execSync(`npx jest e2e-2 --listTests`);
Promise.all(
    String(output)
        .split('\n')
        .filter(line => line !== '')
        .map(async testPath => {
            const testClient = new Docker();
            const runCommand = ['npx', 'jest', testPath.split('guet/')[1]];
            const result = await testClient.run(
                'guettest:0.0.1',
                runCommand,
                process.stdout
            );

            const exitCode = result[0]['StatusCode'];
            return exitCode;
        })
).then(exitCodes => {
    if (exitCodes.find(exitCode => exitCode > 0)) {
        process.exit(1);
    }
});
