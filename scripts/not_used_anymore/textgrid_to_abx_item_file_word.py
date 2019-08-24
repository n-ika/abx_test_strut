# Convert Textgrids to an ABXpy item file for doing
# word ABX (i.e., containing one column, word)
#
# Author: Ewan Dunbar

from __future__ import print_function

from textgrid import TextGrid
import sys, argparse
import os.path as osp

class TextGridError(RuntimeError):
    pass

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs) # FIXME WRAP

def get_intervals(textgrid_fn, tier_name):
    tg = TextGrid()
    tg.read(textgrid_fn)
    try:
        tier_i = tg.getNames().index(tier_name)
    except ValueError:
        raise TextGridError("Cannot find tier named " + tier_name)
    return tg[tier_i]

def is_target_word(word, target_words):
    return word != "" \
            and ((target_words is None) or (word in target_words))

def print_abx_item_file_header():
    print("#file onset offset #item word")

def print_abx_item_file_line(filename, interval, item_id):
    print(filename + " " + str(interval.minTime) + " " \
            + str(interval.maxTime) + " " + str(item_id) \
            + " " + interval.mark)

def BUILD_ARGPARSE():
    parser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--excluded-words', help="List of word targets " \
            "to exclude, separated by comma (defaults to none)", default=[],
            type=str)
    parser.add_argument('--target-words', help="List of word targets " \
            "to include, separated by comma (defaults to all)", default=None,
            type=str)
    parser.add_argument('tier_name', help="Name of TextGrid tier",
            type=str)
    parser.add_argument('textgrid_wavfile_pairs',
            help="pairs of filenames, separated by a comma <TextGrid>,<WavFile>",
            type=str, nargs="+")
    return parser

if __name__ == "__main__":
    parser = BUILD_ARGPARSE()
    args = parser.parse_args(sys.argv[1:])

    print_abx_item_file_header()
    for tw in args.textgrid_wavfile_pairs:
        try:
            f_tg, f_wav = tw.split(",")
        except ValueError:
            eprint(
"""ERROR: Need to provide paired TextGrid/wave file names""".replace(
    "\n", " "))
            sys.exit(1)
        try:
            tier = get_intervals(f_tg, args.tier_name)
        except Exception as e:
            eprint(
"""Problem reading TextGrids: <M>""".replace(
    "<M>", str(e)).replace(
    "\n", " "))
            sys.exit(1)
        index_number = 1  # SEE save_intervals_to_wavs.Praat
        for interval in tier:
            if interval.mark != "":
                if is_target_word(interval.mark, args.target_words) \
                        and not interval.mark in args.excluded_words:
                    # SEE save_intervals_to_wavs.Praat
                    wavfile_stripped = osp.splitext(osp.basename(f_wav))[0]
                    item_id = wavfile_stripped + "_" + str(index_number)
                    print_abx_item_file_line(f_wav, interval, item_id)
                index_number += 1

