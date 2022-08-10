# HexDumpFont

This makes a font that displays all characters as their hexadecimal representation. So:
```
Hello World!
```

In this font will render as:
```
48 65 6C 6C 6F 20 57 6F 72 6C 64 21 0A
```

This is done by changing the characters in the font, the `H` character in the font is `48` for
example. The font always renders the utf-8 encoded bytes for each character; `’` (Unicode 0x2019)
renders as `E2 80 99`.

The font is created using a [fontforge](https://fontforge.org/en-US/) Python script to convert the
DejaVu Sans Mono font to the one that converts some unicode blocks into their hexadecimal 'hexdump'
equivalents.

## Usage
Tested and developed against `fontforge 11:21 UTC 24-Sep-2017`, `libfontforge 20170924` (from Ubuntu
18.04 apt mirrors), confirmed working with fontforge `20190801` (from Ubuntu 20.04).
Run `make` in this directory. This writes the fontforge `sfd` file to the `out` directory, as well
as writing the `.ttf` file there. An example html page that uses this font can be hosted with
`make test_host`.

On Linux, it's easiest to copy the ttf file to the `~/.local/share/fonts/` directory, do note that
in 'fancy' editors that show the font in its own typeface in the fontselector (Inkscape and
OpenOffice), the font is called `48 65 78 44 75 6D 70 46 6F 6E 74 0A`, but probably still sorted
near the 'H'.

