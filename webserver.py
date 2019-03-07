import sys
import os

from zmq.eventloop import ioloop
ioloop.install()

from tornado.web import Application
from tornado.ioloop import IOLoop
ioloop = IOLoop.instance()

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

from ws import PushWebSocket
from http_srv import HttpHandler, HttpHandlerIndex

DEBUG = 1
PROFILE = 0

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

class DmxUiApp(Application):
    def __init__(self, external_ip):
        
        handlers = [
            (r'/ws', PushWebSocket),
            (r"/", HttpHandlerIndex, {"external_ip": external_ip}),
            (r"/(.*)", HttpHandler, {"external_ip": external_ip}),
        ]
        settings = {
            "template_path": os.path.join(os.path.dirname(__file__), 'html/templates'),
            "static_path": os.path.join(os.path.dirname(__file__), 'html/static'),
            "compiled_template_cache": False,
            "debug": True,
        }
        Application.__init__(self, handlers, **settings)

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])

    try:
        desc = "Web server for ar lab"
        parser = ArgumentParser(description="hej", formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]")
        parser.add_argument('--external-ip', default="127.0.1.1", nargs='?', help='external server ip')

        # Process arguments
        args = parser.parse_args()

        verbose = args.verbose

        if verbose > 0:
            print("Verbose mode on")

        application = DmxUiApp(external_ip=args.external_ip)
        application.listen(10001)
        print('starting on port 10001')
        ioloop.start()
        
        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception as e:
        if DEBUG:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
    if DEBUG:
        #sys.argv.append("-h")
        sys.argv.append("-v")
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'webserver.webserver_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())