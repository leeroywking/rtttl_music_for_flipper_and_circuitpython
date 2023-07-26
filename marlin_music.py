from rp2040_audio_formatted.StillDre import song as still_dre
from rp2040_audio_formatted.note_map import note_map

def play_note(note,durr):
    # print(f"playing frequency",note_map[note])
    # simpleio.tone(board.A3, note_map[note], duration=durr)
    freq = note_map[note]
    print(f"M300 S{int(freq)} P{int(durr*1000)}")

def play_song(song):
    title = song["title"]
    print(f"\n\n\n\n\nNow playing:\n    {title}")
    bpm = song["bpm"]
    def_duration = song["duration"]
    def_octave = song["octave"]
    notes = song["notes"]
    seconds_per_whole_note = 60/bpm*4
    for note in notes:
        [duration,letter,octave,dot,sharp] = note
        if not duration:
            duration = def_duration
        true_duration = seconds_per_whole_note / int(duration)
        if dot:
            true_duration = true_duration * 1.5
        if sharp:
            letter = letter+"#"
        if not octave:
            octave = def_octave
        letter = letter + str(octave)
        if "P" in letter:
            letter = "N"
        #print("playing",letter,true_duration)
        play_note(letter,true_duration)

play_song(still_dre)