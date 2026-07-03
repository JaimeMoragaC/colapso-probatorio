# La Ficción de la Ciberseguridad Corporativa — dictamen y pruebas de verificación

Repositorio público del dictamen en derecho **«La Ficción de la Ciberseguridad
Corporativa»** (Jaime Marcelo Moraga Carrasco, 2026),
junto con las pruebas criptográficas que permiten **verificar de forma
independiente su autoría, su fecha de existencia y su integridad** — los mismos
mecanismos de atestación que el propio documento defiende.

> El detalle está en el **Anexo F** del documento. Este README es el resumen operativo.

## Contenido

- **PAPER_v3_Formato_Institucional.pdf** — el dictamen (documento principal).
- **PAPER_v3_trabajo.md** — texto fuente.
- **PAPER_v3_trabajo.md.ots** — prueba OpenTimestamps (anclaje en Bitcoin) del texto.
- **SELLO_2026-07-02.txt** — manifiesto con los SHA-256 de esta versión.
- **allowed_signers** — clave pública del autor, para verificar la firma.
- **CITATION.cff** — cómo citar.

## Verificar (tres comprobaciones)

### 1. Autoría — firma criptográfica del autor
El repositorio incluye la clave pública del autor en `allowed_signers`:
```bash
git -c gpg.ssh.allowedSignersFile=allowed_signers verify-tag sello-paper-2026-07-02
```
Debe devolver *Good "git" signature* con la clave Ed25519
`SHA256:AKDHMiud0xMCcm/tvDqgVBCS+Z/sqc9xiixckjYF6kk`.
(En GitHub, la etiqueta y los commits aparecen además como **"Verified"**.)

### 2. Fecha de existencia — anclada en Bitcoin
```bash
ots verify PAPER_v3_trabajo.md.ots
```
La prueba puede figurar como *pending* hasta que el bloque de Bitcoin la confirma
(unas horas); se completa con `ots upgrade PAPER_v3_trabajo.md.ots`.

### 3. Integridad — el texto no fue alterado
```bash
sha256sum PAPER_v3_trabajo.md      # comparar con SELLO_2026-07-02.txt
```

## La ingeniería no es teoría: ejecútela

La arquitectura de atestación descrita en §6.8.1 tiene una **implementación de
referencia ejecutable** que corre contra un TPM 2.0 real:

→ https://github.com/JaimeMoragaC/attested-signing-ceremony

## Cita

Ver [`CITATION.cff`](CITATION.cff). Moraga Carrasco, J. M. (2026). *La Ficción
de la Ciberseguridad Corporativa*. Dictamen en derecho.

## Licencia

Creative Commons Atribución-NoComercial 4.0 Internacional
([CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/deed.es)).
