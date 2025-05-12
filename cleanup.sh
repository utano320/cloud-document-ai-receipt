

usage() {
    echo "Usage: $0 [--all]"
    echo "  --all    Also delete files in the receipts directory"
    exit 1
}

settings_path="config/settings.json"
receipt_folder="receipts"
renamed_receipt_folder="renamed_receipts"
logs_folder="logs"

if [ -f "$settings_path" ]; then
    receipt_folder=$(grep -o '"receipt_folder": *"[^"]*"' "$settings_path" | cut -d'"' -f4)
    renamed_receipt_folder=$(grep -o '"renamed_receipt_folder": *"[^"]*"' "$settings_path" | cut -d'"' -f4)
    logs_folder=$(grep -o '"logs_folder": *"[^"]*"' "$settings_path" | cut -d'"' -f4)
    
    receipt_folder=${receipt_folder%/}
    renamed_receipt_folder=${renamed_receipt_folder%/}
    logs_folder=${logs_folder%/}
fi

logs_count=0
renamed_receipts_count=0
receipts_count=0

if [ -d "$logs_folder" ]; then
    logs_count=$(find "$logs_folder" -type f -name "*.txt" | wc -l)
    find "$logs_folder" -type f -name "*.txt" -delete
fi

if [ -d "$renamed_receipt_folder" ]; then
    renamed_receipts_count=$(find "$renamed_receipt_folder" -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" \) | wc -l)
    find "$renamed_receipt_folder" -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" \) -delete
fi

if [ "$1" = "--all" ]; then
    if [ -d "$receipt_folder" ]; then
        receipts_count=$(find "$receipt_folder" -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" \) -not -path "$receipt_folder/fixed/*" | wc -l)
        find "$receipt_folder" -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" \) -not -path "$receipt_folder/fixed/*" -delete
    fi
fi

echo "Cleanup completed:"
echo "- Deleted $logs_count txt files from $logs_folder directory"
echo "- Deleted $renamed_receipts_count image files from $renamed_receipt_folder directory"
if [ "$1" = "--all" ]; then
    echo "- Deleted $receipts_count image files from $receipt_folder directory"
else
    echo "- $receipt_folder directory was not cleaned (use --all option to clean it)"
fi
