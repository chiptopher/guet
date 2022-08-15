import { add } from './commands/add';
import { getCommitters } from './commands/get';
import { hook } from './commands/hook';
import { init } from './commands/init';
import { setCommitters } from './commands/set';
import { version } from './version';

export function executeCommand(commandName: string, args: string[]) {
    switch (commandName) {
        case '--version':
        case '-v':
            return version();
        case 'init':
            return init(args);
        case 'add':
            return add(args);
        case 'set':
            return setCommitters(args);
        case 'hook':
            return hook(args);
        case 'get':
            return getCommitters(args);
    }
}
