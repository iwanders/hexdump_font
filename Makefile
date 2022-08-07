SHELL=/bin/bash


all:
	mkdir -p out
	./generate_hexfont.py ./dejavu-fonts/src/DejaVuSansMono.sfd\
	  --pad-space \
	  --font-name HexDumpFont \
	  --family-name "HexDumpFont DejaVu Sans Mono" \
	  --full-name "HexDumpFont DejaVu Sans Mono" \
	  --output ./out/HexDumpFont.sfd ./out/HexDumpFont.ttf

test_host:
	python3 -m http.server
