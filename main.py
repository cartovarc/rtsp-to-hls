import argparse, threading, subprocess

from flask import Flask, send_from_directory, render_template

def start_streaming(source, name):
    print("starting streaming for source %s and name %s" % (source, name))
    ffmpeg_command = 'ffmpeg -i "%s" -hls_time 0.1 -hls_wrap 10 "video/%s.m3u8"' % (source, name)

    proc = subprocess.Popen(ffmpeg_command, shell=True, stdout=subprocess.PIPE)
    line = proc.stdout.readline()
    while line:
        print(line)
        line = proc.stdout.readline()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--sources", "-s", nargs='+', help="set RTSP source")
    parser.add_argument("--names", "-n", nargs='+', help="set name of m3u8 file")
    args = parser.parse_args()

    sources, names = None, None

    if args.sources:
        sources = args.sources
    else:
        raise Exception("No RTSP source provided")

    if args.names:
        names = args.names
    else:
        raise Exception("No m3u8 name provided")

    for source, name in zip(sources, names):
        t = threading.Thread(target=start_streaming, args=[source, name])
        t.daemon = True
        t.start()

    app = Flask(__name__, template_folder='template')

    @app.after_request
    def add_header(response):
        response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response


    @app.route('/')
    def index():
        return render_template('index.html')


    @app.route('/video/<string:file_name>')
    def stream(file_name):
        video_dir = './video'
        return send_from_directory(directory=video_dir, filename=file_name)

    app.run(host="0.0.0.0", port=5001)
