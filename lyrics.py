import time
import pygame
import os

# Initialize pygame mixer
pygame.mixer.init()

# Load the music file
pygame.mixer.music.load('music.mp3')

# Example LRC content
lrc_content = """
[00:07.28]I didn't think you'd understand me
[00:15.51]How could you ever even try?
[00:23.48]I don't wanna tiptoe, but I don't wanna hide
[00:27.99]But I don't wanna feed this monstrous fire
[00:32.25]Just wanna let this story die
[00:36.76]And I'll be alright
[00:39.15]We can't be friends :<
[00:42.34]But I'd like to just pre-etend
[00:46.59]You cling to your papers and pens
[00:50.84]Wait until you like me again
[00:55.09]Wait for your love ❤
[00:58.07]My love, I'll wait for your love ❤❤
[01:04.92]Me and my truth, we sit in silence
[01:12.62]Mmm, baby girl, it's just me and you
[01:21.65]'Cause I don't wanna argue, but I don't wanna bite
[01:26.17]My tongue, yeah, I think I'd rather die
[01:30.15]You got me misunderstood
[01:32.54]But at least I look this good
[01:37.06]We can't be friends :<
[01:40.51]But I'd like to just pre-etend
[01:44.50]You cling to your papers and pens
[01:48.75]Wait until you like me again
[01:52.99]Wait for your love ❤
[01:55.65]My love, I'll wait for your love ❤❤
[02:00.70]I'll wait for your love ❤
[02:03.90]My love, I'll wait for your love
[02:09.75]Know that you made me
[02:13.46]I don't like how you paint me, 
[02:15.30] yet I'm still here hanging 
[02:17.45]Not what you made me
[02:21.70]It's something like a daydream
[02:24.35]But I feel so seen in the night
[02:28.62]So for now, it's only me
[02:30.48]And maybe that's all I need
[02:35.79]We can't be friends
[02:39.24]But I'd like to just pre-etend
[02:42.43]You cling to your papers and pens
[02:47.21]Wait until you like me again
[02:50.95]Wait for your love
[02:54.94]My love, I'll wait for your love
[02:58.65]I'll wait for your love
[03:01.84]My love, I'll wait for your love
[03:07.95]I'll wait for your love
[03:11.93]I'll wait for your love
[03:16.18]I'll wait for your love
[03:19.64]I'll wait for your love
[03:23.62]I'll wait for your love
"""

def parse_lrc(lrc):
    lyrics = []
    for line in lrc.strip().split("\n"):
        time_str, lyric = line.split("]", 1)
        time_str = time_str.strip("[")
        m, s = map(float, time_str.split(":"))
        total_seconds = m * 60 + s
        lyrics.append((total_seconds, lyric.strip()))
    return lyrics

lyrics = parse_lrc(lrc_content)

song_duration = 229  
pygame.mixer.music.play()
start_time = time.time()

console_width = 70
scroll_speed = 0.05
line_speed = 1
road_speed = 1

current_line_index = 0
displayed_lines = []
road_offset = 0

border_top = "╔" + "═" * (console_width - 2) + "╗"
border_bottom = "╚" + "═" * (console_width - 2) + "╝"

# Road layers for moving effect
road_top = "---------- ---------- ----------- -----------  ----------- -------- "
road_middle = "===================================================================="
road_bottom = "---------- ---------- ----------- ----------- ----------- --------- "

while current_line_index < len(lyrics) or displayed_lines:
    elapsed_time = time.time() - start_time
    elapsed_minutes = int(elapsed_time // 60)
    elapsed_seconds = int(elapsed_time % 60)

    # Add new lyrics when their time comes
    while current_line_index < len(lyrics) and elapsed_time >= lyrics[current_line_index][0]:
        _, new_line = lyrics[current_line_index]
        displayed_lines.append({'line': new_line, 'position': console_width - 4})  # Start inside the box
        current_line_index += 1

    # Clear the terminal
    os.system('cls' if os.name == 'nt' else 'clear')

    # new_displayed_lines = []
    # consolidated_lyrics = ""  # Single scrolling row for all lyrics

    # for line_data in displayed_lines:
    #     line_data['position'] -= line_speed  # Move left at the same speed

    #     if line_data['position'] > -len(line_data['line']):  
    #         trimmed_line = line_data['line'][max(0, -line_data['position']):]  
    #         consolidated_lyrics += " " * max(0, line_data['position']) + trimmed_line + "  "  # Space out lyrics

    #         new_displayed_lines.append({'line': trimmed_line, 'position': line_data['position']})

    # displayed_lines = new_displayed_lines



    road_offset = (road_offset + road_speed) % len(road_top)
    road_top_scrolling = road_top[road_offset:] + road_top[:road_offset]
    road_middle_scrolling = road_middle[road_offset:] + road_middle[:road_offset]
    road_bottom_scrolling = road_bottom[road_offset:] + road_bottom[:road_offset]

    output = [border_top]

    timer_text = f"{elapsed_minutes:02}:{elapsed_seconds:02} / {song_duration // 60:02}:{song_duration % 60:02}"
    output.append(f"║ {timer_text.ljust(console_width - 3)}║")

    output.append("║" + " " * (console_width - 2) + "║")

    scrolling_text = [" "] * (console_width - 3)
    new_displayed_lines = []

    for line_data in displayed_lines:
        line_data['position'] -= line_speed

        if line_data['position'] > -len(line_data['line']):  
            visible_part = line_data['line'][max(0, -int(line_data['position'])):]  
            start_pos = max(0, int(line_data['position']))
            
            for i, char in enumerate(visible_part):
                if start_pos + i < len(scrolling_text):
                    scrolling_text[start_pos + i] = char
            
            new_displayed_lines.append(line_data)

    displayed_lines = new_displayed_lines

    while current_line_index < len(lyrics) and elapsed_time >= lyrics[current_line_index][0]:
        _, new_line = lyrics[current_line_index]
        displayed_lines.append({'line': new_line, 'position': console_width - 4})  
        current_line_index += 1  

    output.append(f"║ {''.join(scrolling_text)}║")


    while len(output) < 7:
        output.append("║" + " " * (console_width - 2) + "║")

    output.append(f"║{road_top_scrolling.ljust(console_width - 2)}║")
    output.append(f"║{road_middle_scrolling.ljust(console_width - 2)}║")
    output.append(f"║{road_bottom_scrolling.ljust(console_width - 2)}║")
    output.append(border_bottom)

    print("\n".join(output))
    time.sleep(scroll_speed)

while pygame.mixer.music.get_busy():
    time.sleep(0.1)