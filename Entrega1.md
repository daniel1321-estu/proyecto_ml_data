

**Asunto:** Protocolo de Sustentación Técnica Fase 1: La Terminal es la única Herramienta para la sustentación\
**De:** Profesor *Jorge Blanco*\
**Para:** Ingeniería de Datos – Proyecto ***Data Science**\
**Puntuación:** 20/30

---
---

### Declaración de Principios: "Ingeniería, no solo Código"

Estimados Candidatos a Ingenieros,

Bienvenidos a la Entrega 1. En esta etapa, el objetivo no es mostrarme una carpeta bonita o un notebook con celdas
ejecutadas en VS Code. El objetivo es validar que su proyecto es 
- **reproducible**, 
- **auditable** y
- **automatizable**.

En la industria real, los pipelines de datos (ETL/ELT) no corren desde el IDE visual; corren desde CI/CD (GitHub
Actions, Jenkins), contenedores (Docker/Kubernetes) y en servidores headless (sin interfaz gráfica). Si dependen del
mouse y del entorno visual para mostrar su trabajo, lamento decirles que **no están listos para producción**.

Por lo tanto, para esta entrega, regirán las siguientes normas y que no son negociables:
1.  **La Terminal es la Interfaz Única:** No abrirán la interfaz visual de los archivos de VS Code para mostrar
estructura. Usarán comandos (`tree`, `ls -la`, etc).
2.  **Ejecución por Línea de Comandos:** El pipeline ETL se ejecutará mediante `python script.py` o scripts de
orquestación, **NO** presionando "Play" en Jupyter Notebook.
3.  **Uso de IA como Copiloto:** Deben usar `gemini-cli` durante la presentación para generar comandos de diagnóstico, explicar errores en tiempo real o optimizar sus propios scripts en vivo.

4. **Manejo de Editores por Terminal:** Deben usar `vim` durante la
presentación para editar un archivo del pipeline ETL, aplicar
correcciones en vivo o gestionar cambios sin abandonar la terminal.

---

### Requisitos Técnicos Previos

Antes de la sustentación, asegúrense de tener esto listo:
*   **Entorno:** Windows (Requiere **WSL2** instalado y configurado) / Linux / macOS. *No se aceptará CMD nativo de Windows sin WSL*.
*   **Prohibido:** No pueden usar la consola clásica de Windows (**CMD**
/ `cmd.exe`) ni **PowerShell** para ejecutar los scripts.
¿Por qué les exijo esto? por razones técnicas.
La mayoría de las herramientas de **ETL, DevOps y CI/CD** funcionan en
entornos Linux (servidores, nube, contenedores Docker).
*   **Proyecto:** Generado con la template de `cookiecutter-data-science`.
*   **Herramientas:** `git`, `python` (3.9+), `virtualenv` o `poetry, preferiblemente uv y `gemini-cli` autenticado (`gemini auth`).
*   **Dependencias:** Instalar en un entorno virtual aislado, NOOOOO global.
* Vim instalado

Recomendaciones:
1.  Activen la característica "Subsistema de Linux" en su PC.
2.  Instalen una distribución desde Microsoft Store (ej. **Ubuntu**).
3.  Verifiquen que al abrir la terminal aparezca `ubuntu@nombre-de-pc:~$`
y **NO** `C:\Users\usuario>`.

4.  **Mover el proyecto** a `/home/tu_usuario/` dentro de WSL2.
5.  **Instalar e iniciar Vim** dentro de WSL2.

---

### Flujo de la Sustentación.

La sustentación del avance durará entre 10-15 minutos y consistirá en una demostración en vivo ("Live Coding/Execution"). Ni se les ocurra hacer diapositivas en Pobrepoint para explicar el código, para explicar conceptos teóricos deben desarrollar los esquemas, flujos o arquitecturas con `Mermaid`.

Deben ejecutar los siguientes bloques de comandos secuencialmente:

#### 1. Verificación del Entorno y Estructura (Cookiecutter)

```bash
# 1. Mostrar ubicación actual
pwd

# 2. Mostrar estructura completa (debe verse src/, notebooks/, data/, models/, etc)

tree -a --dirsfirst -I '__pycache__|ipynb_checkpoints'
# deben instalar la utilidad `tree` si no la tienen.
# 3. Verificar versión de Python y entorno virtual
python --version
which python
pip list | grep -i "pandas\|numpy\|requests"
```
*Nota: Asegúrense de estar en la terminal del WSL (Ubuntu).*

#### 2. Estado del Repositorio Git
*Un Ingenieros de verdad mantienen su código versionado.*
```bash
git status
git diff HEAD~1 --name-only # (Mostrar qué archivos se han modificado esta semana)
```

#### 3. Ejecución del Pipeline ETL (Sin Notebooks)
*Aquí está el núcleo de la ingeniería. El Notebook fue para explorar, pero aquí usaremos funciones.*
```bash
# Activar entorno virtual (si no estaba activo)
source venv/bin/activate

# Ejecutar el script principal (ejemplo, deben adaptar según su código)
python src/pipeline/main.py --mode=full
# O paso a paso si modularisaron:
python src/data/ingest.py
python src/transformations/clean_data.py
```
*Requisito:* Deben tener argumentos (`argparse` o `typer`) para que la terminal controle el proceso, no código
"hardcodeado".

#### 4. Verificación de Artefactos (Datos)
*¿Realmente se generaron los datos?*
```bash
# Verificar que existan archivos en data/processed
ls -lh data/processed/
head data/processed/tabla_final.csv # O parquet

# Comprobar integridad rápida (ej. contar líneas)
wc -l data/processed/*.csv
```

#### 5. Interacción con Gemini-CLI (Demostración de IA)
*Deben probar cómo la IA ayuda en el flujo.*
*   **Escenario:** Simulen un error o pidan a Gemini mejorar una función.
    ```bash
    gemini "Revisa este comando para contar registros duplicados en data/processed"
    # O si se rompe el script:
    gemini "Me da KeyError en la función extract_data, ayúdame a arreglarlo y dime qué cambiar en
src/data/ingest.py"
    ```

---

### Criterios de Rechazo
Se calificará como **NO APROBADO** si:
1.  Se abre VS Code para mostrar la estructura de carpetas.
2.  Se ejecuta un `.ipynb` (Notebook) haciendo clic en "Run All".
3.  El código está todo en una sola función gigante dentro de `main.py` sin separación en paquetes (`src/`).
4.  No pueden explicarse los comandos que escriben ("copié y pegué" sin entender el flujo).

¡Éxitos mis Gatos!!!. Quiero ver líneas de comando, logs en consola y precisión técnica.
---
---
# De Retro con los 80´s !!!
---
---
**Nota Final**, Asegúrense de que su sustentación me produzca algo de **adrenalina**, al menos un poquito más de la adrenalina que me produce cuando me bajo de un colchón tirado en el piso.
# 😉
