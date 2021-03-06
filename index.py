
import matlab.engine
from flask import Flask
from flask_restful import Resource, Api, reqparse
from io import IOBase
from werkzeug.datastructures import FileStorage
import wave
import struct
import numpy as np
import os
import soundfile as sf


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



matlab_session = matlab.engine.find_matlab()[0]

eng = matlab.engine.connect_matlab(matlab_session)


class Matlab(Resource):

    def post(self): # HTTP, POST Request
        parse = reqparse.RequestParser()
        parse.add_argument('audio', type=FileStorage, location='files') # Parses the audio data as M4P
        parse.add_argument('name', type=str)

        args = parse.parse_args()

        stream = args['audio']
        path = os.path.join("../Matlab/Sound/", args["name"]+".m4a")
        print(path) # For debug purposes
        outputPath = os.path.join("../Matlab/Sound/", args["name"]+".wav")
        stream.save(os.path.join("../Matlab/Sound/", args["name"]+".m4a"))
        os.system('ffmpeg -i "%s" -t 4 "%s" ' % (path, outputPath)) # Converts the audio to a wav file


        data = eng.classify_input('./Sound/' + args["name"]+".wav") # Calls the Matlab Engine function
        return {'data': data}, 200  # return data and 200 OK code


if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app) # Main loop to initialize our api

    api.add_resource(Matlab, '/')  # '/users' is our entry point for Users
    print("running!")
    app.run()  # run our Flask app
