#!/bin/bash
# Quick SEO Audit Script
# Usage: ./quick_audit.sh <graphql_url> <username> <app_password>
#
# Example:
#   ./quick_audit.sh https://example.com/graphql admin "xxxx xxxx xxxx xxxx"

set -e

GRAPHQL_URL="${1:-$WP_GRAPHQL_URL}"
USERNAME="${2:-$WP_USERNAME}"
APP_PASSWORD="${3:-$WP_APP_PASSWORD}"

if [[ -z "$GRAPHQL_URL" || -z "$USERNAME" || -z "$APP_PASSWORD" ]]; then
    echo "Usage: $0 <graphql_url> <username> <app_password>"
    echo "Or set WP_GRAPHQL_URL, WP_USERNAME, WP_APP_PASSWORD environment variables"
    exit 1
fi

AUTH=$(echo -n "$USERNAME:$APP_PASSWORD" | base64)

echo "=== WordPress SEO Quick Audit ==="
echo "Site: $GRAPHQL_URL"
echo ""

# Fetch posts with SEO data
QUERY='{"query":"{ posts(first: 100) { nodes { databaseId title seo { title metaDesc focuskw } } } }"}'

RESPONSE=$(curl -s "$GRAPHQL_URL" \
    -H "Authorization: Basic $AUTH" \
    -H "Content-Type: application/json" \
    -d "$QUERY")

# Check for errors
if echo "$RESPONSE" | jq -e '.errors' > /dev/null 2>&1; then
    echo "Error fetching data:"
    echo "$RESPONSE" | jq '.errors'
    exit 1
fi

# Parse and analyze
TOTAL=$(echo "$RESPONSE" | jq '.data.posts.nodes | length')
MISSING_TITLE=$(echo "$RESPONSE" | jq '[.data.posts.nodes[] | select(.seo.title == "" or .seo.title == null)] | length')
MISSING_DESC=$(echo "$RESPONSE" | jq '[.data.posts.nodes[] | select(.seo.metaDesc == "" or .seo.metaDesc == null)] | length')
MISSING_KEYPHRASE=$(echo "$RESPONSE" | jq '[.data.posts.nodes[] | select(.seo.focuskw == "" or .seo.focuskw == null)] | length')
SHORT_DESC=$(echo "$RESPONSE" | jq '[.data.posts.nodes[] | select(.seo.metaDesc != null and .seo.metaDesc != "" and (.seo.metaDesc | length) < 120)] | length')
LONG_DESC=$(echo "$RESPONSE" | jq '[.data.posts.nodes[] | select(.seo.metaDesc != null and (.seo.metaDesc | length) > 160)] | length')

echo "📊 Summary"
echo "─────────────────────────────"
printf "Total posts analyzed:    %3d\n" "$TOTAL"
echo ""

echo "❌ Issues Found"
echo "─────────────────────────────"
printf "Missing SEO title:       %3d\n" "$MISSING_TITLE"
printf "Missing meta description:%3d\n" "$MISSING_DESC"
printf "Missing focus keyphrase: %3d\n" "$MISSING_KEYPHRASE"
printf "Description too short:   %3d (< 120 chars)\n" "$SHORT_DESC"
printf "Description too long:    %3d (> 160 chars)\n" "$LONG_DESC"
echo ""

# Calculate score
ISSUES=$((MISSING_TITLE + MISSING_DESC + MISSING_KEYPHRASE))
if [[ $TOTAL -gt 0 ]]; then
    SCORE=$(echo "scale=0; 100 - ($ISSUES * 100 / ($TOTAL * 3))" | bc)
else
    SCORE=0
fi

echo "📈 SEO Health Score: ${SCORE}%"
echo ""

# List posts with issues
if [[ $ISSUES -gt 0 ]]; then
    echo "📝 Posts Needing Attention"
    echo "─────────────────────────────"
    echo "$RESPONSE" | jq -r '.data.posts.nodes[] | select(.seo.title == "" or .seo.title == null or .seo.metaDesc == "" or .seo.metaDesc == null or .seo.focuskw == "" or .seo.focuskw == null) | "ID \(.databaseId): \(.title)"' | head -20
    
    if [[ $ISSUES -gt 20 ]]; then
        echo "... and $((ISSUES - 20)) more"
    fi
fi

echo ""
echo "Run 'python scripts/analyze_seo.py --all' for detailed analysis"
