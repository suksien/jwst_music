import matplotlib.image as mplimg
import matplotlib.pyplot as plt
import numpy as np
from mido import Message, MidiFile, MidiTrack, MetaMessage

def unpack(filename):
    img = mplimg.imread(filename)

    r = img[:,:,0]
    g = img[:,:,1]
    b = img[:,:,2]
    rgb = np.sum(img, axis=2)

    return rgb, img

def convert_to(rgb, map_arr, sum_axis=0):
    # map "rgb" input values to values in "map_arr" input
    rgb_sum = np.sum(rgb, axis=sum_axis)
    rgb_sum_norm = rgb_sum/np.mean(rgb_sum)
    bins = np.linspace(rgb_sum_norm.min(), rgb_sum_norm.max(), len(map_arr))
    ind = np.digitize(rgb_sum_norm, bins, right=True)

    rgb_freq = map_arr[ind]
    return rgb_freq

def create_midi(midi_notes, outfile, channel=10, velocity=64, note_dur=20):

    # channel=10 --> piano
    # velocity=64 --> medium strength for attacking keys
    # note_dur in ticks
    mid = MidiFile()  # filename argument is optional, just create object
    track1 = MidiTrack()
    mid.tracks.append(track1)

    track1.append(MetaMessage('set_tempo', tempo=800000, time=0))
    track1.append(Message('program_change', channel=channel, time=0))

    for i, note in enumerate(midi_notes):
        if i >= len(midi_notes) - 5:
            # slow down towards the end, increases attacking strength to 100
            track1.append(Message('note_on', channel=channel, note=note, velocity=100, time=0))
            track1.append(Message('note_off', channel=channel, note=note, velocity=100, time=note_dur + 100))
        else:
            track1.append(Message('note_on', channel=channel, note=note, velocity=velocity, time=0))
            track1.append(Message('note_off', channel=channel, note=note, velocity=velocity, time=note_dur))

    mid.save(outfile)