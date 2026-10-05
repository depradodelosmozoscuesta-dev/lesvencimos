#!/usr/bin/env bash
# Build Fat Completo release 2.0.19 — SOLO desde /workspace/lesvencimos (canónico).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
case "$ROOT" in
  *lesvacimos*)
    echo "ABORT: cwd/path tipográfico lesvacimos detectado: $ROOT" >&2
    echo "Usa el canónico: /workspace/lesvencimos/android-cascaron" >&2
    exit 2
    ;;
esac
case "$PWD" in
  *lesvacimos*)
    echo "ABORT: PWD tipográfico lesvacimos: $PWD" >&2
    exit 2
    ;;
esac
case "$ROOT" in
  */lesvencimos/android-cascaron|*/lesvencimos/android-cascaron/*) ;;
  *)
    echo "ABORT: expected .../lesvencimos/android-cascaron, got $ROOT" >&2
    exit 2
    ;;
esac
export JAVA_HOME="${JAVA_HOME:-/usr/lib/jvm/java-21-openjdk-amd64}"
export ANDROID_HOME="${ANDROID_HOME:-/workspace/lesvencimos/.android-sdk}"
cd "$ROOT"
EMBED="app/src/main/assets/embed/completo-offline.zip"
EXPECTED_EMBED_MD5="251431ec0feed64c06fecb1001d7f185"
BAD_OLD_FE01_MD5="fe01eac7abf1d3ede6653b892d625716"
BAD_216_MD5="673b9bf813b1638eb0081015eeb8b8a0"
BAD_LIVE_483_MD5="483865a228d3abb518405a8ee5e16f3c"
BAD_K7MAX_MD5="59c51e9882554bbb45e645893fc84202"
BAD_OLD_29B_MD5="29b5760b51bc7486d8250f0521637e1c"
BAD_OLD_3CF1_MD5="3cf1f7c47234f49ef78af16720edefac"
BAD_625_MD5="625e8cec72d1b4a04f312167630da0ac"
BAD_D2DB_MD5="d2db2a4c03671810c985ec5e10698668"
BAD_FB3_MD5="fb3fee7433afd187bb39fb144d8cd160"
BAD_F363_MD5="f363ee8afc2a86a7631cf23be65493ce"
BAD_FAC_MD5="facffac4118718ce04f19704685dd13f"
BAD_K9TODO_MD5="facffac4118718ce04f19704685dd13f"
if [[ ! -f "$EMBED" ]]; then
  echo "ABORT: missing $EMBED" >&2
  exit 3
fi
MD5=$(md5sum "$EMBED" | awk '{print $1}')
if [[ "$MD5" == "3b01f2942147c87990e9d6a5c3ad246f" || "$MD5" == "fe01eac7abf1d3ede6653b892d625716" || "$MD5" == "$BAD_K7MAX_MD5" || "$MD5" == "$BAD_OLD_29B_MD5" || "$MD5" == "$BAD_OLD_3CF1_MD5" || "$MD5" == "$BAD_625_MD5" || "$MD5" == "$BAD_D2DB_MD5" || "$MD5" == "$BAD_FB3_MD5" || "$MD5" == "$BAD_F363_MD5"  || "$MD5" == "$BAD_FAC_MD5" || "$MD5" == "$BAD_LIVE_483_MD5" || "$MD5" == "$BAD_216_MD5" ]]; then
  echo "ABORT: embed is stale/bad $MD5 — refuse; need $EXPECTED_EMBED_MD5" >&2
  exit 3
fi
if [[ "$MD5" != "$EXPECTED_EMBED_MD5" ]]; then
  echo "ABORT: embed MD5 $MD5 != $EXPECTED_EMBED_MD5 (ZIP 2.0.19 v20261005embed-claridad)" >&2
  exit 3
fi
./gradlew assembleRelease "$@"
OUT="app/build/outputs/apk/release/app-release.apk"
if [[ ! -f "$OUT" ]]; then
  echo "ABORT: missing $OUT" >&2
  exit 4
fi
APK_EMBED_MD5=$(unzip -p "$OUT" assets/embed/completo-offline.zip | md5sum | awk '{print $1}')
echo "APK embed MD5: $APK_EMBED_MD5"
if [[ "$APK_EMBED_MD5" != "$EXPECTED_EMBED_MD5" ]]; then
  echo "FAIL: APK embed MD5 $APK_EMBED_MD5 != $EXPECTED_EMBED_MD5 — NOT copying" >&2
  exit 5
fi
cp -f "$OUT" /workspace/lesvencimos/app/lesvencimos-completo.apk
cp -f "$OUT" /workspace/lesvencimos/app/lesvencimos-completo-2.0.19.apk
cp -f "$OUT" /workspace/lesvencimos/app/lesvencimos.apk
cp -f "$OUT" /workspace/lesvencimos/downloads/lesvencimos-completo.apk
cp -f "$OUT" /workspace/lesvencimos/downloads/lesvencimos-completo-2.0.19.apk
cp -f "$OUT" /workspace/lesvencimos/downloads/lesvencimos.apk
echo "OK fat release 2.0.19 (embed gate passed):"
md5sum "$OUT" /workspace/lesvencimos/app/lesvencimos-completo-2.0.19.apk
echo "marker EXPECTED: v20261005embed-claridad"
echo "embed MD5: $APK_EMBED_MD5"
