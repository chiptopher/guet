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

    if (parallel) {
        failed = await runInParallel(testFiles);
    } else {
        failed = await runSequentially(testFiles);
    }

    if (failed) {
        process.exit(1);
    }
}

async function runSequentially(testFiles) {
    let failed = false;
    for (let i = 0; i < testFiles.length; i++) {
        const result = await runForFile(testFiles[i], process.stdout);
        const exitCode = result.exitCode;

        if (exitCode > 0) {
            failed = true;
        }
    }
    return failed;
}

async function runInParallel(testFiles) {
    console.log('Running in parallel'.green);
    const results = await Promise.all(
        testFiles.map(file => runForFile(file, undefined))
    ).then(results =>
        results.map(result => {
            return { ...result };
        })
    );

    const failed = results
        .map(result => result.exitCode)
        .reduce((a, b) => a + b, 0);

    if (failed) {
        console.log('Test failed. See results below:'.red);
    } else {
        console.log('All tests passed :)'.green);
    }

    results.forEach(result => {
        if (result.exitCode > 0) {
            console.log(result.fileName.red);
        } else {
            console.log(result.fileName.green);
        }
    });

    return failed;
}

async function runForFile(fileName, out) {
    const testClient = new Docker();
    const runCommand = ['npx', 'jest', fileName.split('guet/')[1]];
    const result = await testClient.run('guettest:0.0.1', runCommand, out);

    await result[1].remove().catch(error => {
        console.error('Failed to remove container.'.red);
        console.error(error);
    });
    return {
        container: result[1],
        exitCode: result[0]['StatusCode'],
        fileName,
    };
}

main().catch(error => {
    console.error('An unexpected error coccurred:');
    console.error(error);
});
