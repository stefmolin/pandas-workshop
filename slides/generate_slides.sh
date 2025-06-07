#!/usr/bin/env -S uv run --group slides bash

# get paths
SCRIPT=$(realpath "$0")
SLIDES_DIR=$(dirname "$SCRIPT")
REPO_DIR=$(dirname "$SLIDES_DIR")

if [[ "$#" -ne 1 ]]; then
    echo "Specify slide type as argument. Options:"
    echo $(ls -d $SLIDES_DIR/templates/*/ | xargs -n 1 basename | awk -vORS=', ' '{ print $1; }' | sed 's/, $/\n/');
else
    TEMPLATE_TYPE="$1";

    # use nbmerge to combine all slide notebooks into a single notebook
    echo "[nbmerge] Creating a combined notebook for all slides..."
    COMBINED_NOTEBOOK="$SLIDES_DIR/workshop.ipynb"
    nbmerge -o $COMBINED_NOTEBOOK $SLIDES_DIR/*.ipynb;

    # make all slide decks
    jupyter nbconvert \
        --to slides \
        --template=$TEMPLATE_TYPE \
        --TemplateExporter.extra_template_basedirs="$SLIDES_DIR"/templates \
        --output-dir="$SLIDES_DIR"/html \
        "$COMBINED_NOTEBOOK";

    # delete the combined notebook
    echo "Cleaning up..."
    rm $COMBINED_NOTEBOOK

    echo "Done!";
fi


