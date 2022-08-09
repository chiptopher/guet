import { init } from './commadns/init';

export function executeCommand(commandName: string, args: string[]) {
    switch (commandName) {
        case 'init':
            return init(args);
    }
}
