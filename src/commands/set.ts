import { log } from '../native-wrapper';
import { configPath, readJSONFile } from '../utils';

export function setCommitters(args: string[]) {
    const missingInitials = args.filter(
        arg =>
            !readJSONFile(configPath)
                .committers.map(committer => committer.initials)
                .includes(arg)
    );

    if (missingInitials.length > 0) {
        missingInitials.forEach(initials =>
            log(`No committer exists with the initials "${initials}".`, 'error')
        );
        process.exit(1);
    }
}
