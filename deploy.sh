#!/usr/bin/env bash

if ! poetry build; then
  echo "Failed to build pypokedex. Rerun 'poetry build'. Aborting."
  exit 1
fi

echo "Built pypokedex in dist folder"

# Requires rename utility with perl replace support
if ! rename 's/py3/py36/' dist/pypokedex-1.4.0-py3-none-any.whl; then
  echo "Unable to rename built wheel. Aborting."
  exit 1
fi

echo "Renamed wheel"

if ! poetry publish; then
  echo "Failed to publish pypokedex. Rerun 'poetry publish'. Aborting."
  exit 1
fi

echo "Successfully published package to PyPI"
exit 0
