import matlab.engine
from flask import Flask
from flask_restful import Resource, Api, reqparse
from io import IOBase
from werkzeug.datastructures import FileStorage
import wave
import struct
import numpy as np


def loadstereowav(w):

    nchannels, sample_width, sample_rate, nframes, comptype, compname = w.getparams()
    assert nchannels == 2 and sample_width == 2 and comptype == 'NONE'
    frames = w.readframes(nframes * nchannels)
    sound = struct.unpack_from((str(nframes)+'h') * nchannels, frames)
    w.close()
    return sample_rate, nchannels, sample_width, sound


def savestereowav(filename, sample_rate, n_channels, sample_width, sound):
    # Add file parameters
    w1 = wave.open(filename, "w")
    w1.setnchannels(n_channels)
    w1.setsampwidth(sample_width)
    w1.setframerate(sample_rate)
    for i in range(0, len(sound)):
        w1.writeframesraw(struct.pack('<h', sound[i]))  # Copy each frame


eng = matlab.engine.start_matlab()


class Matlab(Resource):
    def get(self):
        data = eng.triarea(20, 10)
        return {'data': data}, 200  # return data and 200 OK code

    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('audio', type=FileStorage, location='files')
        parse.add_argument('name', type=str)

        args = parse.parse_args()

        stream = args['audio'].stream
        wav_file = wave.open(stream, 'rb')

        srate, channels, swidth, sound = loadstereowav(wav_file)
        savestereowav('./sounds/'+args['name'] +
                      '.wav', srate, channels, swidth, sound)

        return {"data": "Saved!"}, 200


if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(Matlab, '/')  # '/users' is our entry point for Users
    print("running!")
    app.run()  # run our Flask app
