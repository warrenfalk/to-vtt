#!/usr/bin/env python

import xml.etree.ElementTree as ET
import base64

def parse_ttml(ttml_content):
    root = ET.fromstring(ttml_content)
    namespace = {'ttml': 'http://www.w3.org/ns/ttml'}
    subtitles = []
    
    for body in root.findall('ttml:body', namespace):
        for div in body.findall('ttml:div', namespace):
            for p in div.findall('ttml:p', namespace):
                begin = convert_time(p.attrib['begin'])
                end = convert_time(p.attrib['end'])
                text = ' '.join(p.itertext())
                subtitles.append((begin, end, text))
                
    return subtitles

def escape_text(text):
  return text.replace("'", "\\'")

# We will process each subtitle and make it appear at most 400ms earlier and stay at most 1200ms longer
expand_backward = 1.0
expand_forward = 2.4
def expand_time(subtitles):
    # But without overlapping the previous or next subtitle
    # We give preference to expanding forward of one than backward of the next
    expanded_subtitles = []
    for i, subtitle in enumerate(subtitles):
        begin, end, text = subtitle
        min_begin = expanded_subtitles[i - 2][1] if i >= 2 else 0
        begin = max(begin - expand_backward, min_begin + 0.01)
        max_end = subtitles[i + 2][0] if i < (len(subtitles) - 2) else float('inf')
        end = min(end + expand_forward, max_end - 0.01)
        expanded_subtitles.append((begin, end, text))
    return expanded_subtitles

def ttml_to_jscues(subtitles):
    jscues_content = "let cues = [\n"
    for subtitle in subtitles:
        begin, end, text = subtitle
        jscues_content += f"[{round(begin, 3)},{round(end, 3)},'{escape_text(text)}'],\n"
    jscues_content += "];\n"
    return jscues_content

def convert_time(ttml_time):
    if ttml_time.endswith('t'):
        ticks = int(ttml_time[:-1])
        milliseconds = ticks / 10000
        seconds = milliseconds / 1000
        return seconds
    else:
        hours, minutes, seconds = map(float, ttml_time.split(':'))
        return hours * 3600 + minutes * 60 + seconds


def vtt_to_data_url(vtt_content):
    vtt_bytes = vtt_content.encode('utf-8')
    base64_vtt = base64.b64encode(vtt_bytes).decode('utf-8')
    data_url = f"data:text/vtt;base64,{base64_vtt}"
    return data_url

def read_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

if __name__ == '__main__':
    ttml_content = read_from_file('input.ttml')

    subtitles = expand_time(parse_ttml(ttml_content))
    cue_js = ttml_to_jscues(subtitles)
    print("""let video = document.querySelector('video')""")
    print("""video.crossOrigin = true;""")
    print("""let track = video.addTextTrack('subtitles', 'Spanish', 'es')""")
    print("""track.mode = 'showing'""")
    print(cue_js)
    print("""cues.forEach(cue => track.addCue(new VTTCue(...cue)))""")
