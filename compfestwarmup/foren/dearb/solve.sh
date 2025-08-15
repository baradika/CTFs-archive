#!/bin/bash

# Create directory for extracted files
mkdir -p extracted_secrets

# Extract all secret*.zip files
for zipfile in secret*.zip; do
    num=$(echo "$zipfile" | sed 's/secret\([0-9]*\)\.zip/\1/')
    txtfile="secret${num}.txt"
    
    if [ ! -f "$txtfile" ]; then
        echo "Extracting $zipfile..."
        unzip -q -o "$zipfile" -d extracted_secrets/ 2>/dev/null
        
        if [ $? -ne 0 ]; then
            echo "Fixing header of $zipfile..."
            printf '\x50\x4B\x03\x04' | dd of="$zipfile" conv=notrunc bs=1 count=4 2>/dev/null
            unzip -q -o "$zipfile" -d extracted_secrets/ 2>/dev/null
        fi
    fi
done

# Combine all secret*.txt files
combined_secret=""
for txtfile in $(ls secret*.txt extracted_secrets/secret*.txt 2>/dev/null | sort -V); do
    if [ -f "$txtfile" ]; then
        content=$(cat "$txtfile" | tr -d '\n')
        combined_secret="${combined_secret}${content}"
    fi
done

# Output and save the result
echo -e "\n=== Combined Secret ==="
echo "$combined_secret"
echo -e "======================="

echo "$combined_secret" > final_secret.txt
echo "Saved to final_secret.txt"
