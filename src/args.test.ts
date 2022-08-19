import { separateFlags } from './args';
describe('separateFlags', () => {
    it('should separate flags from args in order', () => {
        const [args, flags] = separateFlags([
            'arg1',
            '--flag1',
            'arg2',
            '--flag2',
            'arg3',
            'arg4',
        ]);
        expect(args).toEqual(['arg1', 'arg2', 'arg3', 'arg4']);
        expect(flags).toEqual(['--flag1', '--flag2']);
    });
});
