#!/usr/bin/env bash
# Repository sanitization script for TechCon365Dallas2025
# Removes all personal information, secrets, and local paths for public release

set -e  # Exit on error

echo "🔒 Sanitizing TechCon365Dallas2025 repository for public release"
echo "================================================================"

# Backup important files that should remain sensitive
if [[ -f "lmstudio-mcp-config.json" ]]; then
    echo "📁 Backing up local config file..."
    cp lmstudio-mcp-config.json lmstudio-mcp-config.json.backup
fi

# Files to sanitize (all markdown files and python files)
FILES_TO_SANITIZE=(
    "*.md"
    "*.py"
    "mcp-servers/**/*.md"
    "mcp-servers/**/*.py"
)

# Create list of all files to process
TEMP_FILE_LIST=$(mktemp)
for pattern in "${FILES_TO_SANITIZE[@]}"; do
    find . -name "$pattern" -type f >> "$TEMP_FILE_LIST"
done

# Remove duplicates and exclude security_check.py (it contains regex patterns)
sort "$TEMP_FILE_LIST" | uniq | grep -v "security_check.py" > "${TEMP_FILE_LIST}.clean"
FILE_LIST="${TEMP_FILE_LIST}.clean"

echo "📊 Found $(wc -l < "$FILE_LIST") files to sanitize"

# Sanitization patterns
echo "🧹 Applying sanitization patterns..."

# 1. Remove CLIENT_SECRET values
echo "  - Removing CLIENT_SECRET values..."
while IFS= read -r file; do
    if [[ -f "$file" ]]; then
        # Replace actual secret with placeholder
        sed -i.bak 's/h6F8Q~HGKG-vOuYyMFgEo9x9_NpnMQ4XaccNEb~_/YOUR_CLIENT_SECRET_HERE/g' "$file"
        # Replace CLIENT_SECRET="value" with CLIENT_SECRET="YOUR_CLIENT_SECRET_HERE" 
        sed -i.bak 's/CLIENT_SECRET.*=.*"[^"]*"/CLIENT_SECRET="YOUR_CLIENT_SECRET_HERE"/g' "$file"
        # Replace CLIENT_SECRET": "value" with CLIENT_SECRET": "YOUR_CLIENT_SECRET_HERE"
        sed -i.bak 's/CLIENT_SECRET":\s*"[^"]*"/CLIENT_SECRET": "YOUR_CLIENT_SECRET_HERE"/g' "$file"
    fi
done < "$FILE_LIST"

# 2. Replace personal email with generic
echo "  - Replacing personal email addresses..."
while IFS= read -r file; do
    if [[ -f "$file" ]]; then
        sed -i.bak 's/fabian@adotob\.com/your-email@your-domain.com/g' "$file"
    fi
done < "$FILE_LIST"

# 3. Replace company domain with generic
echo "  - Replacing company domain..."
while IFS= read -r file; do
    if [[ -f "$file" ]]; then
        # Replace adotob.com but not in the context of explaining what was removed
        sed -i.bak '/❌.*adotob\.com.*→/!s/adotob\.com/your-domain.com/g' "$file"
    fi
done < "$FILE_LIST"

# 4. Replace personal file paths with generic
echo "  - Replacing personal file paths..."
while IFS= read -r file; do
    if [[ -f "$file" ]]; then
        sed -i.bak 's|/Users/fabswill/miniforge3/bin/python3|/path/to/your/python3|g' "$file"
        sed -i.bak 's|/Users/fabswill/ReposClaudeCode/TechCon365Dallas2025|/path/to/TechCon365Dallas2025|g' "$file"
        sed -i.bak 's|/Users/fabswill/|/Users/yourname/|g' "$file"
    fi
done < "$FILE_LIST"

# 5. Clean up specific references that should be generic
echo "  - Cleaning up documentation-specific references..."
while IFS= read -r file; do
    if [[ -f "$file" ]]; then
        # Replace "fabian@adotob.com confirmed" with generic version
        sed -i.bak 's/fabian@your-domain\.com confirmed/user account confirmed/g' "$file"
        # Replace specific tenant references
        sed -i.bak 's/(your-domain\.com tenant only)/(your tenant)/g' "$file"
        sed -i.bak 's/(your-domain\.com domain)/(your domain)/g' "$file"
    fi
done < "$FILE_LIST"

# 6. Fix test files - remove actual secrets from test files
echo "  - Sanitizing test files..."
if [[ -f "test_graph_mcp.py" ]]; then
    # Replace the entire env section in test file
    sed -i.bak 's/"CLIENT_SECRET": "YOUR_CLIENT_SECRET_HERE"/"CLIENT_SECRET": "not-needed-for-device-flow"/g' test_graph_mcp.py
fi

# 7. Update README files to use template patterns
echo "  - Updating README files with template patterns..."
for readme in mcp-servers/*/README.md; do
    if [[ -f "$readme" ]]; then
        # Replace export CLIENT_SECRET with template version
        sed -i.bak 's/export CLIENT_SECRET="YOUR_CLIENT_SECRET_HERE"/# export CLIENT_SECRET="not-needed-for-device-flow"  # Only needed for client credentials flow/g' "$readme"
    fi
done

# 8. Clean up .cache references (conversation logs)
echo "  - Removing references to local cache files..."
while IFS= read -r file; do
    if [[ -f "$file" ]]; then
        sed -i.bak 's|/Users/yourname/\.cache/lm-studio/conversations/[0-9]*\.conversation\.json|~/local-lm-studio-logs/conversation.json|g' "$file"
    fi
done < "$FILE_LIST"

# Remove backup files
echo "🧽 Cleaning up backup files..."
find . -name "*.bak" -delete

# Update .gitignore to ensure local files are protected
echo "🛡️  Updating .gitignore for better protection..."
cat >> .gitignore << 'EOF'

# Additional security for public repo
*.backup
.cache/
**/token_cache*.json
lmstudio-mcp-config.json
claude_desktop_config.json
EOF

# Clean up temp files
rm -f "$TEMP_FILE_LIST" "${TEMP_FILE_LIST}.clean"

echo ""
echo "✅ Repository sanitization complete!"
echo "📋 Summary of changes:"
echo "   - CLIENT_SECRET values → 'YOUR_CLIENT_SECRET_HERE'"
echo "   - Personal email → 'your-email@your-domain.com'"  
echo "   - Company domain → 'your-domain.com'"
echo "   - Personal paths → '/path/to/...' or '/Users/yourname/...'"
echo "   - Local cache files → Generic references"
echo ""
echo "🔍 Next steps:"
echo "   1. Run: python security_check.py"
echo "   2. Verify all references are generic"
echo "   3. Test template files work correctly"
echo "   4. Ready for public GitHub release!"