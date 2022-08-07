#!/usr/bin/env fontforge

import fontforge
import sys
import argparse

# Glyph id for 0-9a-f
def h(v):
    return "hf_{:x}".format(v)

# Convert ascii to glyph id for 0-9a-f
def ascii_to_glyph(z):
    return h(int(z.lower(), 16))

def copy_font_properties(src, dst):
    dst.ascent = src.ascent
    dst.bitmapSizes = src.bitmapSizes
    dst.changed = src.changed
    # dst.copyright = src.copyright
    dst.descent = src.descent
    dst.design_size = src.design_size
    dst.em = src.em
    dst.encoding = src.encoding
    # dst.familyname = src.familyname + "_hexfont"
    dst.fontlog = src.fontlog
    # dst.fullname = src.fullname + "_hexfont"
    dst.strokedfont = src.strokedfont
    dst.strokewidth = src.strokewidth
    dst.upos = src.upos
    dst.uwidth = src.uwidth
    dst.version = src.version
    dst.verticalBaseline = src.verticalBaseline
    dst.weight = src.weight

def copy_building_block(src, src_codepoint, dst, name):
    src.selection.select(src_codepoint)
    src.copy()
    v = dst.createChar(-1, name)
    sel = dst.selection.select(name)
    dst.paste()
    v.glyphname = name

def create_hexadecimal_codepoint(hf, cp, append_space=False):
    # Retrieve or obtain the char we are going to update.
    c = hexfont.createChar(cp)

    unicode_char = unichr(cp)
    try:
        unicode_bytes = unicode_char.encode("utf-8")
        v = "".join(["{:0>2X}".format(i) for i in bytearray(unicode_bytes)])
    except UnicodeDecodeError as e:
        v = "{:X}".format(cp)

        # Make sure it is padded with zero's on the left to an odd value.
        if len(v) % 2 != 0:
            v = "0" + v

    # Split it by chunks of two.
    hexdisplay = [v[(i*2):((i + 1)*2)] for i in range(len(v)/2)]
    # print(hexdisplay)

    current_offset = 0;
    for i, b in enumerate(hexdisplay):
        left = b[0]
        right = b[1]
        left_glyph = list(hf.selection.select(ascii_to_glyph(left)).byGlyphs)[0]


        transform = [1, 0, 0,
                     1, current_offset, 0];
        c.addReference(ascii_to_glyph(left), transform)

        current_offset += left_glyph.width

        transform = [1, 0, 0,
                     1, current_offset, 0];
        c.addReference(ascii_to_glyph(right), transform)

        right_glyph = list(hf.selection.select(ascii_to_glyph(right)).byGlyphs)[0]
        current_offset += right_glyph.width

        if ((i + 1) != len(hexdisplay)) or append_space:
            space_glyph = list(hf.selection.select("hf_space").byGlyphs)[0]
            transform = [1, 0, 0,
                         1, current_offset, 0];
            c.addReference("hf_space", transform)
            current_offset += space_glyph.width


    c.width = current_offset

# Adapted from:
# https://stackoverflow.com/questions/63872752/fontforge-python-add-kerning-classes
# http://designwithfontforge.com/en-US/Spacing_Metrics_and_Kerning.html
# Oh, default kerning must always be zero, lets do it by pairs afterall.
def add_kerning(hf):
    space_glyph = list(hf.selection.select("hf_space").byGlyphs)[0]

    offsets = [space_glyph.width] * (256 ** 2)
    offsets_tuple = tuple(offsets)

    hf.addLookup("kern", "gpos_pair", (), [["kern", [["latn", ["dflt"]]]]])
    c1 = tuple([list(hf.selection.select(i).byGlyphs)[0].glyphname for i in range(256)])

    hf.addKerningClass("kern", "kern-1", c1, c1, offsets_tuple)

# add_kerning(hexfont)
# Attempt to output 131088 into a 16-bit field. It will be truncated and the file may not be useful.
# Lookup sub table, kern-1 in kern, is too big. Will not be useable.
# We could split the lookups into different lookups... but the whole n**2 is... unfortunate
# if we want to support unicode characters.


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Convert font to hexdump font.')
    parser.add_argument('fontpath', help='The font to convert into the hexdump font')
    parser.add_argument('--pad-space', action='store_true',default=False,
                    help='Add spaces to all characters (default:%(default)s).')
    args = parser.parse_args()


    # Open the base font we're picking glyphs from.
    deja_base = fontforge.open(args.fontpath)

    hexfont = fontforge.font()
    copy_font_properties(deja_base, hexfont)

    # Copy the primitives.
    for i in range(16):
        copy_building_block(deja_base, ord("{:x}".format(i).upper()), hexfont, h(i))
    copy_building_block(deja_base, ord(" "), hexfont, "hf_space")

    # Populate the first byte fully.
    # for i in range(256):
        # create_hexadecimal_codepoint(hexfont, i, append_space=args.pad_space);

    """
https://en.wikipedia.org/wiki/Unicode_block#List_of_blocks
 0 BMP	U+0000..U+007F	Basic Latin[g]	128	128	Latin (52 characters), Common (76 characters)
 0 BMP	U+0080..U+00FF	Latin-1 Supplement[h]	128	128	Latin (64 characters), Common (64 characters)
 0 BMP	U+0100..U+017F	Latin Extended-A	128	128	Latin
 0 BMP	U+0180..U+024F	Latin Extended-B	208	208	Latin

 0 BMP	U+2000..U+206F	General Punctuation	112	111	Common (109 characters), Inherited (2 characters)
 0 BMP	U+2070..U+209F	Superscripts and Subscripts	48	42	Latin (15 characters), Common (27 characters)
 0 BMP	U+20A0..U+20CF	Currency Symbols	48	33	Common
 0 BMP	U+20D0..U+20FF	Combining Diacritical Marks for Symbols	48	33	Inherited
 0 BMP	U+2100..U+214F	Letterlike Symbols	80	80	Greek (1 character), Latin (4 characters), Common (75 characters)
 0 BMP	U+2150..U+218F	Number Forms	64	60	Latin (41 characters), Common (19 characters)
    """
    def populate_block(lower, upper):
        for i in range(lower, upper):
            create_hexadecimal_codepoint(hexfont, i, append_space=args.pad_space);

    populate_block(0x0000, 0x007f)
    populate_block(0x0080, 0x00FF)
    populate_block(0x0100, 0x017F)
    populate_block(0x0180, 0x024F)
    populate_block(0x2000, 0x206F)

    populate_block(0x20A0, 0x20CF)

        

    # Dump output.
    hexfont.fontname="HexFont"
    hexfont.save("/tmp/HexFont.sfd")
    hexfont.generate("/tmp/HexFont.ttf")