#!/bin/bash

ENUM_SOURCE="https://github.com/123FLO321/POGOProtos-Swift/raw/master/Sources/POGOProtos/Enums/Enums-Form.pb.swift"
GM_SOURCE="https://raw.githubusercontent.com/pokemongo-dev-contrib/pokemongo-game-master/master/versions/latest/GAME_MASTER.json"
OUTFILE="form2enum.py"
GENDIR="$(readlink -f $(dirname $0))"
OUTDIR="$PWD"

TMPDIR=$(mktemp -d)
cd "$TMPDIR"

wget -q "$ENUM_SOURCE"
wget -q "$GM_SOURCE"

echo 'form2enum = {' > "$GENDIR/$OUTFILE"
egrep '^\s+[0-9]+:' Enums-Form.pb.swift | less | sed 's/\.same(proto: //;s/)//' >> "$GENDIR/$OUTFILE"
echo '}' >> "$GENDIR/$OUTFILE"

python3 "$GENDIR/assetmap.py" --game_master="$TMPDIR/GAME_MASTER.json" > "$OUTDIR"/assetmap.json
python3 "$GENDIR/formmap.py" > "$OUTDIR"/formmap.json

rm -r "$TMPDIR"
