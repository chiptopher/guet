type LogLevel = 'info' | 'error';

export function log(message: string, level?: LogLevel) {
    switch (level) {
        case 'error':
            console.log(message.red);
            break;
        case 'info':
        default:
            console.log(message.green);
            break;
    }
}
