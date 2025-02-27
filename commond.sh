#!/bin/sh
rename(){
    cd /app
    python -c "from rename import rename; from tree import read_tree; rename(True, read_tree())"
}

recover(){
    cd /app
    python -c "from rename import rename; from tree import read_tree; rename(False, read_tree())"
}

show_help(){
    echo 'rename Rename files'
    echo 'recover Restore the file name to the original one before the rename'
}

case "$1" in
    rename)
        rename
        ;;
    recover)
        recover
        ;;
    *)
        show_help
        ;;
esac
