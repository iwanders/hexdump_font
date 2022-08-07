#!/usr/bin/env fontforge

import fontforge
import sys


# Glyph id for 0-9a-f
def h(v):
    return "hf_{:x}".format(v)

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

def create_hexadecimal_codepoint(hf, cp):
    # Retrieve or obtain the char we are going to update.
    c = hexfont.createChar(cp)

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

        if ((i + 1) != len(hexdisplay)):
            space_glyph = list(hf.selection.select("hf_space").byGlyphs)[0]
            transform = [1, 0, 0,
                         1, current_offset, 0];
            c.addReference("hf_space", transform)
            current_offset += space_glyph.width


    c.width = current_offset


# Open the base font we're picking glyphs from.
deja_base = fontforge.open(sys.argv[1])

hexfont = fontforge.font()
copy_font_properties(deja_base, hexfont)

# Copy the primitives.
for i in range(16):
    copy_building_block(deja_base, ord("{:x}".format(i).upper()), hexfont, h(i))
copy_building_block(deja_base, ord(" "), hexfont, "hf_space")

# Populate the first byte fully.
for i in range(256):
    create_hexadecimal_codepoint(hexfont, i);

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

add_kerning(hexfont)


# Dump output.
hexfont.fontname="HexFont"
hexfont.save("/tmp/HexFont.sfd")
hexfont.generate("/tmp/HexFont.ttf")