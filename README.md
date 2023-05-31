# preprocessor-util

`python3 preproc.py O_APPEND fnctl.h`

is equivalent to:

`echo O_APPEND | gcc -include fcntl.h -E - | more`

> Works with Python 3.6+

## Usage

The first argument is whatever you wish to send to the preprocessor.

Arguments after that are headers to include.
Both system-wide headers and relative/absolute path headers work.

`python3 preproc.py true stdbool.h` Result: `1`

If no includes parameters are given, a [default list](#configuration) is used.

`python3 preproc.py true` Result: `1`

## Integration with [`bat`](https://github.com/sharkdp/bat)

This program tries to display the result with `bat`.
If that fails, it falls back to a simple print.
This behavior can be [configured](#configuration) off.

## Configuration

There are a few constants at the top of `preproc.py` that may be tweaked, give it a look!
