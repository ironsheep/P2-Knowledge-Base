#!/bin/bash

# Archive Migration Script
# Renames existing YYYYMMDD archives to YYMMDD_HHMM format
# Uses file modification time to add timestamp

PROCESSED_DIR="./inbox/processed"

echo "Archive Migration Tool"
echo "====================="
echo

if [ ! -d "$PROCESSED_DIR" ]; then
    echo "No processed directory found at $PROCESSED_DIR"
    exit 1
fi

echo "Found archives to migrate:"
ls -d "$PROCESSED_DIR"/20* 2>/dev/null || { echo "No archives found"; exit 0; }

echo
read -p "Migrate these archives to new format? (y/n) " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Migration cancelled"
    exit 0
fi

for dir in "$PROCESSED_DIR"/20*; do
    if [ -d "$dir" ]; then
        # Extract date from directory name
        dirname=$(basename "$dir")
        
        # Check if it's old format (8 digits: YYYYMMDD)
        if [[ "$dirname" =~ ^[0-9]{8}$ ]]; then
            year=${dirname:0:4}
            month=${dirname:4:2}
            day=${dirname:6:2}
            
            # Get modification time of the directory
            mod_time=$(stat -f "%Sm" -t "%H%M" "$dir" 2>/dev/null || stat -c "%y" "$dir" 2>/dev/null | cut -d' ' -f2 | cut -d: -f1-2 | tr -d :)
            
            # If we can't get mod time, use sequential numbering
            if [ -z "$mod_time" ]; then
                counter=0
                mod_time=$(printf "%02d%02d" $((counter/60)) $((counter%60)))
                while [ -d "$PROCESSED_DIR/${year:2}${month}${day}_${mod_time}" ]; do
                    counter=$((counter + 1))
                    mod_time=$(printf "%02d%02d" $((counter/60)) $((counter%60)))
                done
            fi
            
            # Create new name in YYMMDD_HHMM format
            new_name="${year:2}${month}${day}_${mod_time}"
            new_path="$PROCESSED_DIR/$new_name"
            
            # Check if target already exists
            if [ -d "$new_path" ]; then
                echo "⚠️  Skipping $dirname - $new_name already exists"
            else
                mv "$dir" "$new_path"
                echo "✅ Migrated: $dirname → $new_name"
            fi
        else
            echo "ℹ️  Skipping $dirname - already in new format"
        fi
    fi
done

echo
echo "Migration complete!"
echo "Current archives:"
ls -d "$PROCESSED_DIR"/* 2>/dev/null | xargs -n1 basename | sort