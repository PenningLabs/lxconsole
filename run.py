from lxconsole import app
import os
import argparse

# Parse command-line arguments
parser=argparse.ArgumentParser(description="LXConsole Args Parser")
parser.add_argument('--port', type=int)
parser.add_argument('--host', type=str)
args, extra = parser.parse_known_args()

# Use environment vars for the server (defaulting if not provided)
port = os.environ.get("FLASK_RUN_PORT") or 5000
host = os.environ.get("FLASK_RUN_HOST") or '0.0.0.0'

# Override vars with command-line args
port = args.port or port
host = args.host or host

if __name__ == '__main__':
    app.run(debug=False, host=host, port=port)
