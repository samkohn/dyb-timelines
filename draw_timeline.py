import argparse
import csv
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

HEIGHT = 3*inch
WIDTH = 10*inch
MARGIN = 1*inch
LINE_SIZE = 0.5*inch
RECT_SIZE = 0.3*inch
RECT_ALPHA = 0.2
PROMPT_WINDOW = 400000  # ns
MUWS_WINDOW = 400000

def draw_marker(c, time, timescale, t0, line_color, text):
    start_x = t0 + time*timescale
    c.setStrokeColorRGB(*line_color, 1)
    c.setLineWidth(4)
    c.line(start_x, HEIGHT/2 - LINE_SIZE, start_x,
            HEIGHT/2 + LINE_SIZE)
    c.setFillColorRGB(0, 0, 0, 1)
    c.setFont("Helvetica-Bold", 30)
    c.drawString(start_x, HEIGHT/2 + LINE_SIZE + 0.1*inch, text)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(start_x, HEIGHT/2 - LINE_SIZE - 0.4*inch,
            str(int(time/1000)) + 'us')
    return

def draw_window(c, time, timescale, t0, window_dt, stroke_color,
        fill_color):
    start_x = t0 + time*timescale
    c.setStrokeColorRGB(*stroke_color, 1)
    c.setFillColorRGB(*fill_color, RECT_ALPHA)
    c.setLineWidth(2)
    c.rect(start_x, HEIGHT/2 - RECT_SIZE, window_dt*timescale,
            2 * RECT_SIZE, stroke=1, fill=1)
    return

def draw_prompt(c, time, timescale, t0):
    stroke_color = (0, 1, 0)
    fill_color = (0, 1, 0)
    draw_window(c, time, timescale, t0, PROMPT_WINDOW, stroke_color,
            fill_color)
    draw_marker(c, time, timescale, t0, stroke_color, "P")

def draw_delayed(c, time, timescale, t0):
    stroke_color = (0, 0, 1)
    fill_color = (0, 1, 0)
    draw_window(c, time, timescale, t0, PROMPT_WINDOW, stroke_color,
            fill_color)
    draw_marker(c, time, timescale, t0, stroke_color, "D")

def draw_wsmuon(c, time, timescale, t0):
    stroke_color = (1, 0, 0)
    fill_color = (1, 0, 0)
    draw_window(c, time, timescale, t0, PROMPT_WINDOW, stroke_color,
            fill_color)
    draw_marker(c, time, timescale, t0, stroke_color, "mu")


def main(events, outfile):
    c = canvas.Canvas(outfile, (WIDTH, HEIGHT))
    c.setLineWidth(4)
    c.line(MARGIN, HEIGHT/2, WIDTH-MARGIN, HEIGHT/2)
    min_timestamp = float('inf')
    max_timestamp = 0
    for event in events:
        event['timestamp'] = int(event['timestamp'])
        min_timestamp = min(min_timestamp, event['timestamp'])
        max_timestamp = max(max_timestamp, event['timestamp'])
    print(min_timestamp)
    print(max_timestamp)
    max_timestamp += PROMPT_WINDOW
    timescale = (WIDTH-3*MARGIN)/(max_timestamp - min_timestamp)
    t0 = 1.5 * MARGIN
    print(timescale)
    for event in events:
        event['type'] = event['type'].strip()
        event['timestamp'] -= min_timestamp
        if event['type'] == 'promptlike':
            draw_prompt(c, event['timestamp'], timescale, t0)
        elif event['type'] == 'delayedlike':
            draw_delayed(c, event['timestamp'], timescale, t0)
        elif event['type'] == 'wsmuon':
            draw_wsmuon(c, event['timestamp'], timescale, t0)
        else:
            print(repr(event['type']))
    c.save()



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile')
    parser.add_argument('-o', '--outfile')
    args = parser.parse_args()
    with open(args.infile, 'r') as f:
        reader = csv.DictReader(f)
        events = list(reader)
    main(events, args.outfile)
