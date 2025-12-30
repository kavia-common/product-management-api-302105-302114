#!/bin/bash
cd /home/kavia/workspace/code-generation/product-management-api-302105-302114/product_crud_backend
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

