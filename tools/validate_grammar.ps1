<#
.SYNOPSIS
    Validate SQF.tmLanguage on Windows

.DESCRIPTION
    Ensures SQF.tmLanguage is a well-formed XML/plist file.
    Uses PowerShell’s built-in XML parser to catch errors.
    Exits with code 0 on success, non-zero on error.
#>

param (
    [string]$GrammarPath = "SQF.tmLanguage"
)

if (-Not (Test-Path $GrammarPath)) {
    Write-Error "File not found: $GrammarPath"
    exit 1
}

try {
    # Load as XML to validate structure
    [xml]$xml = Get-Content -Raw -Path $GrammarPath
    if (-not $xml) {
        Write-Error "Failed to parse $GrammarPath as XML."
        exit 1
    }
    Write-Output "$GrammarPath is well-formed XML."
    exit 0
}
catch {
    Write-Error "XML validation failed: $($_.Exception.Message)"
    exit 1
}
