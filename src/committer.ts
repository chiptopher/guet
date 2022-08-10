export interface Committer {
    email: string;
    fullName: string;
    initials: string;
}

export function removeCommitterWithInitials(
    initials: string,
    committers: Committer[]
) {
    return committers.filter(committer => committer.initials !== initials);
}
