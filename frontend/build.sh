#!/bin/sh
set -eu
: "${API_BASE_URL:?Vercel 환경변수 API_BASE_URL을 설정하세요.}"
printf 'window.API_BASE_URL="%s";\n' "$API_BASE_URL" > frontend/config.js
