

usage() {
    echo "Usage: $0 [--all]"
    echo "  --all    Also delete files in the receipts directory"
    exit 1
}

logs_count=0
renamed_receipts_count=0
receipts_count=0

if [ -d "logs" ]; then
    logs_count=$(find logs -type f -name "*.txt" | wc -l)
    find logs -type f -name "*.txt" -delete
fi

if [ -d "renamed_receipts" ]; then
    renamed_receipts_count=$(find renamed_receipts -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" \) | wc -l)
    find renamed_receipts -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" \) -delete
fi

if [ "$1" = "--all" ]; then
    if [ -d "receipts" ]; then
        receipts_count=$(find receipts -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" \) | wc -l)
        find receipts -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" \) -delete
    fi
fi

echo "Cleanup completed:"
echo "- Deleted $logs_count txt files from logs directory"
echo "- Deleted $renamed_receipts_count image files from renamed_receipts directory"
if [ "$1" = "--all" ]; then
    echo "- Deleted $receipts_count image files from receipts directory"
else
    echo "- receipts directory was not cleaned (use --all option to clean it)"
fi
