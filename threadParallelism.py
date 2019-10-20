import os
import time
import numpy
import librosa
import shutil
from concurrent.futures import ThreadPoolExecutor

path = "unknown"
audio_path = "unknown"

def getAndWrite(file):
    y, rate = librosa.load(file)
    mfcc = librosa.feature.mfcc(y=y, sr=rate)
    new_file = path + file[len(audio_path):-4]
    numpy.save(new_file, mfcc)

print("Give path to the directory with audio files")
audio_path = input()
print("Give path to the directory where to put MFCC features")
path = input()
path = path + "/mfcc"
if os.path.exists(path):
    shutil.rmtree(path)
begin = time.time()
for cur_dir, directories, files in os.walk(audio_path):
    os.mkdir(path + cur_dir[len(audio_path):])
file_names = librosa.util.find_files(audio_path)
file_names = numpy.asarray(file_names)
with ThreadPoolExecutor(max_workers=3) as pool:
    pool.map(getAndWrite, file_names)
print("time used:", time.time() - begin)
