#!/usr/bin/env bash
# Recordatorio + actualización del sello OpenTimestamps.
# Lo dispara un timer systemd-user una vez, tras la confirmación en Bitcoin.
# Actualiza las pruebas .ots del monorepo Y del repo público del paper.
# NO commitea/pushea (para no depender del agente SSH en el entorno del timer);
# te avisa para que confirmes tú.
OTS="/home/jaime/Descargas/antigravity/.venv/bin/ots"
MONO="/home/jaime/Descargas/antigravity/paper_ficcion_juridica"
CLEAN="/home/jaime/Descargas/colapso-probatorio"
LOG="$MONO/.ots_upgrade.log"

{
  echo "===== $(date '+%Y-%m-%d %H:%M:%S %Z') ====="
  if [ -d "$MONO" ]; then
    cd "$MONO" && "$OTS" upgrade SELLO_2026-07-02.txt.ots PAPER_v3_trabajo.md.ots 2>&1
  fi
  if [ -d "$CLEAN" ]; then
    cd "$CLEAN" && "$OTS" upgrade PAPER_v3_trabajo.md.ots PAPER_v3_Formato_Institucional.pdf.ots SELLO_2026-07-02.txt.ots 2>&1
  fi
  echo "(fin del intento)"
} >> "$LOG" 2>&1

notify-send -u critical "📌 Paper: sello Bitcoin + HITO Zenodo" \
  "1) Sello Bitcoin (.ots) actualizado — revisa .ots_upgrade.log; en el repo público: git add *.ots && commit && push. 2) HITO ZENODO: buen momento para depositar la v1 y obtener el DOI (reservar DOI -> meterlo en el paper -> publicar). Pídeselo a Claude." 2>/dev/null || true

exit 0
