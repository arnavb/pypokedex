#!/usr/bin/env bash

if ! poetry build; then
  echo "Failed to build pypokedex. Rerun 'poetry build'. Aborting."
  exit 1
fi

echo "Built pypokedex in dist folder"

# Requires rename utility with perl replace support
if ! rename 's/py3/py36/' dist/pypokedex-1.5.1-py3-none-any.whl; then
  echo "Unable to rename built wheel. Aborting."
  exit 1
fi

echo "Renamed wheel"

# Needed to that env token is read properly. See:
# https://github.com/python-poetry/poetry/issues/2801#issuecomment-672705712
poetry config http-basic.pypi "__token__" "${POETRY_PYPI_TOKEN_PYPI}"

if ! poetry publish; then
  echo "Failed to publish pypokedex. Rerun 'poetry publish'. Aborting."
  exit 1
fi

echo "Successfully published package to PyPI"
exit 0
