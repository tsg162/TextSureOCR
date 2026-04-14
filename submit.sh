#!/usr/bin/env bash
# Submit TextSureOCR to gpu1 via gpuharbor.
# Encodes app.py and tests.py into the job spec and submits.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVER="${1:-gpu1}"

echo "Encoding app.py …"
B64_APP=$(base64 -w0 "$SCRIPT_DIR/app.py")

echo "Encoding tests.py …"
B64_TESTS=$(base64 -w0 "$SCRIPT_DIR/tests.py")

echo "Patching job YAML …"
python3 -c "
import sys
b64_app = sys.argv[1]
b64_tests = sys.argv[2]
with open('$SCRIPT_DIR/job-setup.yaml') as f:
    content = f.read()
content = content.replace('PLACEHOLDER_BASE64_APP', b64_app)
content = content.replace('PLACEHOLDER_BASE64_TESTS', b64_tests)
with open('/tmp/textsure-job.yaml', 'w') as f:
    f.write(content)
print('Job YAML written to /tmp/textsure-job.yaml')
" "$B64_APP" "$B64_TESTS"

echo "Submitting to ${SERVER} …"
gpuharbor submit /tmp/textsure-job.yaml --server "$SERVER"
