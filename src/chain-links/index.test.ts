/* eslint-disable @typescript-eslint/no-empty-function */
import { ChainLink } from '.';
import { ClosureChainLink } from '../command';

describe('ChainLink', () => {
    describe('next', () => {
        let first: ChainLink;
        let second: ChainLink;
        let third: ChainLink;

        let result: ChainLink;

        beforeEach(() => {
            first = new ClosureChainLink(() => {});
            second = new ClosureChainLink(() => {});
            third = new ClosureChainLink(() => {});
            result = first.next(second).next(third);
        });

        it('puts the given command at the end of the chain', () => {
            expect(first.following).toEqual(second);
            expect(second.following).toEqual(third);
            expect(third.following).toBeUndefined();
        });

        it('returns the head of the chain', () => {
            expect(result).toBe(first);
        });
    });
});
