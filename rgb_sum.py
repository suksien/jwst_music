import argparse
import utils
import numpy as np

parser = argparse.ArgumentParser(description='generate music based on RGB sum of image', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--inputimage', type=str, required=True, help="input image")
parser.add_argument('--outputmidi', type=str, required=True, help="output midi")
parser.add_argument('--channel', type=int, required=False, default=10, help="midi channel")
parser.add_argument('--velocity', type=int, required=False, default=64, help="how hard to play keys")
parser.add_argument('--note_dur', type=int, required=False, default=20, help="duration of note in tick unit")

args = parser.parse_args()

filename = args.inputimage
outfile = args.outputmidi
channel = args.channel
velocity = args.velocity
note_dur = args.note_dur

rgb, img = utils.unpack(filename)
midi_piano_notes = np.arange(21, 109, 1) # range of midi values for 88 piano keys (https://newt.phys.unsw.edu.au/jw/notes.html)
rgb_midi_notes = utils.convert_to(rgb, midi_piano_notes, sum_axis=1)
utils.create_midi(rgb_midi_notes, outfile, channel=channel, velocity=velocity, note_dur=note_dur)