#!/usr/bin/env bash
# Vigila PAPER_v3_trabajo.md y regenera el PDF cuando lo editas a mano.
# No requiere inotify-tools ni sudo: hace polling del mtime con `stat`.
# No toca los permisos del .md (puedes seguir editando mientras corre).
#
# Uso:
#   ./watch_paper.sh                                   # primer plano (Ctrl-C para parar)
#   setsid nohup ./watch_paper.sh >/dev/null 2>&1 &    # segundo plano (sobrevive a la terminal)
#   ./watch_paper.sh --stop                            # detener el watcher en segundo plano
set -u
cd "$(dirname "$0")"

FILE="PAPER_v3_trabajo.md"
LOG=".watcher.log"
LOCK=".watcher.lock"

log(){ echo "[watcher] $(date +%H:%M:%S) — $*" | tee -a "$LOG"; }

# --stop: matar el watcher en ejecución
if [ "${1:-}" = "--stop" ]; then
  if [ -e "$LOCK" ] && kill "$(cat "$LOCK" 2>/dev/null)" 2>/dev/null; then
    echo "Watcher detenido (PID $(cat "$LOCK"))."
  else
    echo "No hay watcher en ejecución."
  fi
  rm -f "$LOCK"
  exit 0
fi

# Evitar dos watchers simultáneos
if [ -e "$LOCK" ] && kill -0 "$(cat "$LOCK" 2>/dev/null)" 2>/dev/null; then
  echo "Ya hay un watcher corriendo (PID $(cat "$LOCK")). Saliendo."
  exit 0
fi
echo $$ > "$LOCK"
trap 'rm -f "$LOCK"; log "watcher detenido"; exit 0' INT TERM EXIT

log "watcher iniciado — vigilando $FILE"
last=$(stat -c %Y "$FILE" 2>/dev/null || echo 0)

while true; do
  sleep 1.5
  now=$(stat -c %Y "$FILE" 2>/dev/null || echo 0)
  [ "$now" = "$last" ] && continue

  # Debounce: esperar a que el editor termine de guardar (mtime estable)
  while sleep 0.6; do
    chk=$(stat -c %Y "$FILE" 2>/dev/null || echo 0)
    [ "$chk" = "$now" ] && break
    now=$chk
  done

  log "Cambio detectado, regenerando PDF..."
  if ./build_pdf.sh >>"$LOG" 2>&1; then
    log "PDF actualizado ✓"
  else
    log "ERROR en build_pdf.sh — revisa $LOG"
  fi
  last=$(stat -c %Y "$FILE" 2>/dev/null || echo 0)
done
