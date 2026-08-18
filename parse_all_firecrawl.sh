#!/bin/bash
# Parse all 85 PDFs with Firecrawl
# Usage: bash parse_all_firecrawl.sh

export FIRECRAWL_API_KEY=fc-09839c86656e491b88e934561e085fba
PDF_DIR="public/data/session-pdfs"
OUT_DIR=".firecrawl"

mkdir -p "$OUT_DIR"

total=$(ls "$PDF_DIR"/*.pdf | wc -l)
count=0
errors=0

for pdf in $(ls "$PDF_DIR"/*.pdf | sort); do
    filename=$(basename "$pdf" .pdf)
    outfile="$OUT_DIR/${filename}.md"
    
    # Skip if already parsed
    if [ -f "$outfile" ]; then
        echo "⏭️  $filename (déjà parsé)"
        count=$((count + 1))
        continue
    fi
    
    echo "📄 Parsing $filename..."
    firecrawl parse "$pdf" -o "$outfile" 2>/dev/null
    
    if [ -f "$outfile" ]; then
        size=$(wc -c < "$outfile")
        echo "✅ $filename ($size bytes)"
        count=$((count + 1))
    else
        echo "❌ $filename (erreur)"
        errors=$((errors + 1))
    fi
    
    # Pause every 10 to avoid rate limits
    if [ $((count % 10)) -eq 0 ]; then
        echo "⏳ Pause 2s..."
        sleep 2
    fi
done

echo ""
echo "=== RÉSULTAT ==="
echo "Total: $total"
echo "Parsés: $count"
echo "Erreurs: $errors"
