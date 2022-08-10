import { add } from './commands/add';
import { init } from './commands/init';
import { setCommitters } from './commands/set';

export function executeCommand(commandName: string, args: string[]) {
    switch (commandName) {
        case 'init':
            return init(args);
        case 'add':
            return add(args);
        case 'set':
            return setCommitters(args);
    }
}
