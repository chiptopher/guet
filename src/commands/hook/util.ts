import { Committer } from '../../committer';

export function appendCoAuthoredBy(
    currentMessage: string,
    committersToAdd: Committer[]
): string {
    const cleanMessage =
        stripTrailingEmptyLines(
            stripPreviousCoAuthoredByLines(currentMessage.split('\n'))
        ).join('\n') + '\n';

    return cleanMessage + '\n' + newCoAuthoredByLines(committersToAdd) + '\n';
}

function newCoAuthoredByLines(committers: Committer[]): string {
    return committers
        .map(
            committer =>
                `Co-authored-by: ${committer.fullName} <${committer.email}>`
        )
        .join('\n');
}

function stripPreviousCoAuthoredByLines(lines: string[]): string[] {
    return lines.filter(line => !line.includes('Co-authored-by: '));
}

function stripTrailingEmptyLines(lines: string[]): string[] {
    const copy = [...lines];
    while (copy[copy.length - 1] === '') {
        copy.pop();
    }
    return copy;
}
