SHELL=/bin/bash


all:
	mkdir -p out
	./generate_hexfont.py ./dejavu-fonts/src/DejaVuSansMono.sfd\
	  --pad-space \
	  --font-name HexDumpFont \
	  --family-name "HexDumpFont DejaVu Sans Mono" \
	  --full-name "HexDumpFont DejaVu Sans Mono" \
	  --copyright-file "OFL.txt" \
	  --output ./out/HexDumpFont.sfd ./out/HexDumpFont.ttf ./out/HexDumpFont.otf ./out/HexDumpFont.woff

test_host:
	python3 -m http.server
