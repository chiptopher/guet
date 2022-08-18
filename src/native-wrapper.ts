type LogLevel = 'info' | 'error' | 'success' | 'warn';

export function log(message: string, level?: LogLevel) {
    switch (level) {
        case 'error':
            console.log(message.red);
            break;
        case 'warn':
            console.log(message.yellow);
            break;
        case 'success':
            console.log(message.green);
            break;
        case 'info':
        default:
            console.log(message.white);
            break;
    }
}
