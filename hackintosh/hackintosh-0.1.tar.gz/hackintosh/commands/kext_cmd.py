from hackintosh import *


@click.group(help='All kext related commands')
def cli():
    cleanup()


@cli.resultcallback()
def post(ctx):
    unzip()


@cli.command(short_help='Download kexts.')
@click.option('-e', '--essential', is_flag=True, help='Download essential kexts to support laptop startup.')
@click.argument('kexts', nargs=-1, type=click.STRING)
@pass_context
def download(ctx, kexts, essential):
    if essential:
        for k in ctx.config['kext']['essential']:
            download_rehabman(k)

    for k in kexts:
        if k in ctx.config['kext']['supported']:
            download_rehabman(k)


@cli.command(short_help='Download kexts for some laptop.')
@pass_context
def laptop(ctx):
    for k in ctx.laptop['kexts']:
        download_rehabman(k)
        info(f'{k} downloaded')


@cli.command(short_help='Download kext for external device')
@click.option('-t', '--type', required=True, type=click.Choice(['wifi', 'bluetooth', 'combo']))
@click.option('-d', '--device', required=True, help='Choose the external device')
@pass_context
def device(ctx, type, device):
    devices = ctx.config['external_device'][type.lower()]

    for d in devices:
        for k in d.keys():
            if k == device:
                for kext in d[k]['kexts']:
                    download_rehabman(kext)

                cprint('Clover kexts patches:', color='blue')
                for p in d[k]['clover']['kexts_to_patch']:
                    for k, v in p.items():
                        cprint(f'{k}=', end='')
                        cprint(v, color='white')
                    print()
                break


@cli.command(short_help='Show all supported kexts.')
@pass_context
def supported(ctx):
    cprint('Supported kexts:', color='blue')

    for k in ctx.config['kext']['supported']:
        cprint(k)

    cprint('Supported devices:', color='blue')

    for k in ctx.config['external_device'].keys():
        cprint(f'{k}:', 'blue', end='')
        for d in ctx.config['external_device'][k]:
            cprint(",".join(d.keys()))
        else:
            print('')
