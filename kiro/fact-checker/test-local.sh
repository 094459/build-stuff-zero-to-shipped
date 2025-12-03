#!/bin/bash
set -e

echo "Starting fact-checker container locally..."
finch run -d --name fact-checker-test -p 8080:8080 fact-checker:latest

echo "Container started. Access the application at http://localhost:8080"
echo "To stop: finch stop fact-checker-test"
echo "To remove: finch rm fact-checker-test"
