import { add } from './commands/add';
import { init } from './commands/init';

export function executeCommand(commandName: string, args: string[]) {
    switch (commandName) {
        case 'init':
            return init(args);
        case 'add':
            return add(args);
    }
}
