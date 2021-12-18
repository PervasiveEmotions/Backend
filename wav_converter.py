
import os
import argparse

from pydub import AudioSegment

dirpath = "./sounds"
filepath = "./sounds/default.m4a"
filename = "default.m4a"


file_extension_final = 'm4a'
try:
    track = AudioSegment.from_file(filepath,
                                    file_extension_final)
    wav_filename = filename.replace(file_extension_final, 'wav')
    wav_path = dirpath + '/converted/' + wav_filename
    print('CONVERTING: ' + str(filepath))
    file_handle = track.export(wav_path, format='wav')
    os.remove(filepath)
except:
    print("ERROR CONVERTING " + str(filepath))
