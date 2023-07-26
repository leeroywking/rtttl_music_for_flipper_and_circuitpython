from distutils.log import error
from fileinput import filename
import os

DIR = "./rtttl3"

song_files = []
for filename in os.listdir(DIR):
    with open(os.path.join(DIR,filename),"r") as f:
        try:
            text = f.read()
            song_files.append(text)
        except:
            error(filename)



def parse_note(note):
    '''
    input format should look like any of the following "2p" "8a" "16g." "16f6"
    '''
    note_list = []
    for char in note:
        note_list.append(char)
    #Kinds of notes
    # 16g -> in standard octave 1/16
    # 2p -> 1/2 pause
    # 16f#6 -> f# in 6th octave for 1/16 duration
    # 16g. -> dot note g for 1/16
    letter = ""
    for char in note_list:
        if char in "abcdefgp":
            letter = char
    if letter == "":
        print("note wrong:",note)
        return None
    letter_idx = note_list.index(letter)
    duration = "".join(note_list[:letter_idx])
    octave = "".join(note_list[letter_idx+1:])
    letter = letter.upper()
    # print( f"{duration}{letter}{octave}")
    
    return f"{duration}{letter}{octave}"


def parse_note_rp2040(note):
    '''
    input format should look like any of the following "2p" "8a" "16g." "16f6"
    '''
    note_list = []
    for char in note:
        note_list.append(char)
    #Kinds of notes
    # 16g -> in standard octave 1/16
    # 2p -> 1/2 pause
    # 16f#6 -> f# in 6th octave for 1/16 duration
    # 16g. -> dot note g for 1/16
    letter = ""
    for char in note_list:
        if char in "abcdefgp":
            letter = char
    if letter == "":
        print("note wrong:",note)
        return None
    letter_idx = note_list.index(letter)
    duration = "".join(note_list[:letter_idx])
    octave = "".join(note_list[letter_idx+1:])
    # example octave "" or "#.5"
    dot = False
    sharp = False
    if "." in octave:
        octave = octave.replace(".","")
        dot = True
    if "#" in octave:
        octave = octave.replace("#","")
        sharp = True
    letter = letter.upper()
    # print( f"{duration}{letter}{octave}")
    
    return [duration,letter,octave,dot,sharp]

def convert_file_flipper_format(file_str):
    while file_str[-1] == "\n" or file_str[-1] ==",":
        file_str = file_str[:-1]
        # print("removed cruft")

    split_file = file_str.split(":")
    title = split_file[0]
    meta_data = split_file[1].split(",")
    duration = meta_data[0].split("=")[1]
    octave = meta_data[1].split("=")[1]
    bpm = meta_data[2].split("=")[1]
    notes = split_file[2].split(",")
    parsed_notes = []
    for note in notes:
        parsed_notes.append(parse_note(note))
        pass
    # print(title)
    joined_notes = ", ".join(parsed_notes)
    return title, f"Filetype: Flipper Music Format\nVersion: 0\nBPM: {bpm}\nDuration: {duration}\nOctave: {octave}\nNotes: {joined_notes}\n"

def convert_file_rp2040_format(file_str):
    while file_str[-1] == "\n" or file_str[-1] ==",":
        file_str = file_str[:-1]
        # print("removed cruft")

    split_file = file_str.split(":")
    title = split_file[0]
    meta_data = split_file[1].split(",")
    duration = meta_data[0].split("=")[1]
    octave = meta_data[1].split("=")[1]
    bpm = meta_data[2].split("=")[1]
    notes = split_file[2].split(",")
    parsed_notes = []
    for note in notes:
        parsed_notes.append(parse_note_rp2040(note))
        # pass
    # print(title)
    # joined_notes = ", ".join(parsed_notes)
    return title, f"song = {{'title':'{title}','bpm':{bpm},'duration':{duration},'octave':{octave},'notes':{parsed_notes}}}"



# convert_file_flipper_format(song_files[0])

# for song in song_files:
#     try:
#         title, output = convert_file_flipper_format(song)
#         with open(f"./flipper_audio_formatted/{title}.fmf", "w") as f:
#             f.write(output)
#         print(output)
#     except:
#         error("couldn't do song:")

for song in song_files:
    try:
        title, output = convert_file_rp2040_format(song)
        with open(f"./rp2040_audio_formatted/{title}.py", "w") as f:
            f.write(output)
            pass
        # print(output)
    except:
        error("couldn't do song:")
