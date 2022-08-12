/* eslint-disable @typescript-eslint/no-var-requires */
const { execSync } = require('child_process');

const colors = require('colors');
const Docker = require('dockerode');

const output = execSync(`npx jest e2e-2 --listTests`);

colors.enable();
async function main() {
    let failed = false;

    let filterText;

    let parallel = false;

    if (process.argv.includes('--filter')) {
        const index = process.argv.indexOf('--filter') + 1;
        filterText = process.argv[index];
    }

    if (process.argv.includes('--parallel')) {
        parallel = true;
    }

    const testFiles = String(output)
        .split('\n')
        .filter(line => line !== '')
        .filter(line => {
            if (filterText) {
                return line.includes(filterText);
            } else {
                return line;
            }
        });

    failed = await (parallel
        ? runInParallel(testFiles)
        : runSequentially(testFiles));

    if (failed) {
        process.exit(1);
    }
}

async function runSequentially(testFiles) {
    let failed = false;
    for (let i = 0; i < testFiles.length; i++) {
        const result = await runForFile(testFiles[i], process.stdout);
        const exitCode = result[0]['StatusCode'];

        if (exitCode > 0) {
            failed = true;
        }
    }
    return failed;
}

async function runInParallel(testFiles) {
    console.log('Running in parallel'.green);
    const failed = Boolean(
        await Promise.all(
            testFiles.map(file => runForFile(file, undefined))
        ).then(results =>
            results
                .map(result => {
                    const exitCode = result[0]['StatusCode'];
                    return exitCode;
                })
                .reduce((a, b) => a + b, 0)
        )
    );

    if (failed) {
        console.log('Encountered an error'.red);
    }

    return failed;
}

async function runForFile(fileName, out) {
    const testClient = new Docker();
    const runCommand = ['npx', 'jest', fileName.split('guet/')[1]];
    const result = await testClient.run('guettest:0.0.1', runCommand, out);

    result[1].remove();
    return result;
}

main().catch(console.error);
