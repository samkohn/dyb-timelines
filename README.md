Daya Bay event timelines
========================

This is a simple module that can be imported or executed to draw basic
timelines in PDF format.

![Example timeline](https://raw.githubusercontent.com/samkohn/dyb-timelines/master/example.png)

To install once you've cloned the repository, just run

```
pip install .
```

To uninstall run

```
pip uninstall dyb-timelines
```

The script is very simple:

```
$ python -m draw_timeline -i <input CSV file> -o <output PDF file>
```

The input CSV file should have a header row which has at least the
columns "type" and "timestamp". The timestamps should be in nanoseconds
and do not have to start at 0. (The scale will start at the earliest
timestamp in the file.) Valid types are currently "promptlike",
"delayedlike", and "wsmuon". All other types are (silently) discareded
when generating the graphic.

The script currently generates graphics whose coincidence and veto
windows correspond to the THU nH
IBD candidate selection.

The graphics engine is Report Lab's PDFGen module.

If you want to customize the window lengths to
a different selection, you can ``import draw_timeline`` and write your
own logic that:

 1. Computes the appropriate time scale (pixels per nanosecond)
 and determines an position (in pixels) for t0 (default = ``1.5 *
 draw_timeline.MARGIN``);
 2. Reads in your event list (e.g. using ``csv.DictReader``) and
 subtracts off a t0;
 3. Creates a ``pdfgen.canvas.Canvas`` object;
 4. Calls the appropriate combination of ``draw_marker`` and
 ``draw_window`` based on each event / combination of events. (You could
 imagine only drawing time windows for delayed-like events, for
 example.) and,
 5. Saves the canvas object.

The signatures for ``draw_window`` and ``draw_marker`` are:

```
draw_marker(c, time, timescale, t0, line_color, text)
draw_window(c, time, timescale, t0, window_dt, stroke_color, fill_color)
```

- c: The pdfgen Canvas object
- time: The timestamp where the marker should go, expressed as number of
  nanoseconds since t0
- timescale: The number of pixels per nanosecond
- t0: The x position (in pixels from the right edge of the canvas)
  corresponding to t0
- line_color: A 3-tuple of (R, G, B) fractions (between 0 and 1
  inclusive) to determine the color of the event marker
- text: The text label for the marker. Note: timestamp labels are added
  automatically and are expressed in microseconds
- stroke_color: A 3-tuple of (R, G, B) fractions (between 0 and 1
  inclusive) to determine the color of the outline of the window
- fill_color: A 3-tuple of (R, G, B) fractions (between 0 and 1
  inclusive) to determine the fill color of the window. Note: will be
  partially transparent

