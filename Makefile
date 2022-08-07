SHELL=/bin/bash


all:
	./generate_hexfont.py ./dejavu-fonts/src/DejaVuSansMono.sfd\
	  --pad-space \
	  --font-name HexDumpFont \
	  --family-name "HexDumpFont DejaVu Sans Mono" \
	  --full-name "HexDumpFont DejaVu Sans Mono" \
	  --output /tmp/HexDumpFont.sfd /tmp/HexDumpFont.ttf
