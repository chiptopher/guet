export class UnexpectedError extends Error {
    constructor(reason: string) {
        super(`An error has occurred for the following reason: ${reason}`);
    }
}
