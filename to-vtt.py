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
                begin = p.attrib['begin']
                end = p.attrib['end']
                text = ''.join(p.itertext())
                subtitles.append((begin, end, text))
                
    return subtitles

def ttml_to_vtt(subtitles):
    vtt_content = "WEBVTT\n\n"
    
    for subtitle in subtitles:
        begin, end, text = subtitle
        vtt_content += f"{convert_time(begin)} --> {convert_time(end)}\n"
        vtt_content += f"{text}\n\n"
    
    return vtt_content

def convert_time(ttml_time):
    if ttml_time.endswith('t'):
        ticks = int(ttml_time[:-1])
        milliseconds = ticks / 10000
        seconds = milliseconds / 1000
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:06.3f}".replace('.', ',')
    else:
        hours, minutes, seconds = map(float, ttml_time.split(':'))
        return f"{int(hours):02}:{int(minutes):02}:{seconds:06.3f}".replace('.', ',')


def vtt_to_data_url(vtt_content):
    vtt_bytes = vtt_content.encode('utf-8')
    base64_vtt = base64.b64encode(vtt_bytes).decode('utf-8')
    data_url = f"data:text/vtt;base64,{base64_vtt}"
    return data_url

def convert_ttml_to_data_url(ttml_content):
    subtitles = parse_ttml(ttml_content)
    vtt_content = ttml_to_vtt(subtitles)
    data_url = vtt_to_data_url(vtt_content)
    return data_url

def read_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

if __name__ == '__main__':
    ttml_content = read_from_file('input.ttml')

    subtitles = parse_ttml(ttml_content)
    vtt_content = ttml_to_vtt(subtitles)
    print(vtt_content)
    data_url = vtt_to_data_url(vtt_content)

    print(data_url)
