import streamlink_cli.main as cli
import streamlink
import sys
import os
from .config import conf


def cli_main(output):

    error_code = 0
    parser = cli.build_parser()

    cli.setup_args(parser, ignore_unknown=True)
    cli.args.output=output
    cli.args.url='https://pccold'
    cli.args.stream=['default']
    # print(cli.args)


    # Console output should be on stderr if we are outputting
    # a stream to stdout.
    if cli.args.stdout or cli.args.output == "-":
        console_out = sys.stderr
    else:
        console_out = sys.stdout

    # We don't want log output when we are printing JSON or a command-line.
    silent_log = any(getattr(cli.args, attr) for attr in cli.QUIET_OPTIONS)
    log_level = cli.args.loglevel if not silent_log else "none"
    cli.setup_logging(console_out, log_level)
    cli.setup_console(console_out)

    cli.setup_streamlink()
    cli.setup_plugin_args(cli.streamlink, parser)
    path=os.path.abspath(os.path.dirname(__file__))[:-6]+'plugins'
    print('dir',path)
    cli.load_plugins([path])

    # update the logging level if changed by a plugin specific config
    log_level = cli.args.loglevel if not silent_log else "none"
    cli.logger.root.setLevel(log_level)

    cli.setup_http_session()

    try:
        cli.setup_options()
        cli.handle_url()
    except KeyboardInterrupt:
        # Close output
        if cli.output:
            cli.output.close()
        cli.console.msg("Interrupted! Exiting...")
        error_code = 130
    finally:
        if cli.stream_fd:
            try:
                cli.log.info("Closing currently open stream...")
                cli.stream_fd.close()
            except KeyboardInterrupt:
                error_code = 130
   
    sys.exit(error_code)