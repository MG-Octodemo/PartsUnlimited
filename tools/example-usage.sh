#!/bin/bash
# Example usage of the Code Documentation Generator

echo "Code Documentation Generator - Example Usage"
echo "============================================="
echo

# Basic usage example
echo "1. Basic analysis of PartsUnlimited codebase:"
echo "python3 code-documentation-generator.py ../PartsUnlimited-aspnet45/"
echo

# Advanced usage example  
echo "2. Generate documentation with 5 workflows and save to file:"
echo "python3 code-documentation-generator.py ../PartsUnlimited-aspnet45/ --workflows 5 --output partsunlimited-docs.md"
echo

# Run the basic example
echo "Running basic analysis..."
python3 code-documentation-generator.py ../PartsUnlimited-aspnet45/ --workflows 2

echo
echo "Example completed. See README.md for more usage options."