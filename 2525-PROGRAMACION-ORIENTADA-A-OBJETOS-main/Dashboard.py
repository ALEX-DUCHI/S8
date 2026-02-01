import os
import subprocess
import sys
from datetime import datetime

UNIDADES = {
    '1': 'Unidad 1',
    '2': 'Unidad 2',
}

RUTA_BASE = os.path.dirname(__file__)
HISTORIAL_EJECUCION = []

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')


def pausar():
    input("\nPresiona Enter para continuar...")


def validar_ruta(ruta):
    return os.path.exists(ruta)

def registrar_historial(ruta_script):
    HISTORIAL_EJECUCION.append({
        "script": ruta_script,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
def mostrar_historial():
    limpiar_pantalla()
    print("=" * 50)
    print(" HISTORIAL DE EJECUCIONES")
    print("=" * 50)

    if not HISTORIAL_EJECUCION:
        print(" Todavía no se ha ejecutado ningún script.")
    else:
        for i, item in enumerate(HISTORIAL_EJECUCUCION, start=1):
            print(f"{i}. {os.path.basename(item['script'])} | {item['fecha']}")

    pausar()



def mostrar_codigo(ruta_script):
    # Asegúrate de que la ruta al script es absoluta
    ruta_script_absoluta = os.path.abspath(ruta_script)
    try:
        with open(ruta_script_absoluta, 'r', encoding='utf-8') as archivo:
            codigo = archivo.read()
            print("\n" + "="*50)
            print(f" Código del script: {os.path.basename(ruta_script)}")
            print("="*50 + "\n")
            print(codigo)
            return codigo
    except FileNotFoundError:
        print("El archivo no se encontró.")
        return None
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None
    



def ejecutar_codigo(ruta_script):
    try:
        print(f"\nEjecutando el script...\n")
        subprocess.run([sys.executable, ruta_script], check=False)
        registrar_historial(ruta_script)
    except Exception as e:
        print(f"Ocurrió un error al ejecutar el código: {e}")

def abrir_en_vscode(ruta_script):
    try:
        subprocess.run(["code", ruta_script], check=False)
        print(" Script abierto en VSCode.")
    except Exception:
        print(" No se pudo abrir VSCode. Revisa que el comando 'code' funcione.")

def buscar_scripts(ruta_sub_carpeta):
    scripts = [f.name for f in os.scandir(ruta_sub_carpeta)
               if f.is_file() and f.name.endswith('.py')]

    if not scripts:
        print(" No hay scripts en esta carpeta.")
        pausar()
        return

    palabra = input("\n🔍 Escribe parte del nombre del script: ").strip().lower()
    resultados = [s for s in scripts if palabra in s.lower()]

    limpiar_pantalla()
    print("=" * 50)
    print(" RESULTADOS DE BÚSQUEDA")
    print("=" * 50)

    if not resultados:
        print(" No se encontró ningún script con ese nombre.")
    else:
        for i, s in enumerate(resultados, start=1):
            print(f"{i} - {s}")

    pausar()


def mostrar_menu():
    # Define la ruta base donde se encuentra el dashboard.py

    while True:
        limpiar_pantalla()
        print("=" * 50)
        print(" DASHBOARD - MENÚ PRINCIPAL")
        print("=" * 50)
        for key, nombre in UNIDADES.items():
            print(f"{key} - {nombre}")
        print("\nH - Ver historial de ejecuciones")
        print("R - Refrescar menú")
        print("0 - Salir")

        eleccion_unidad = input("\nElige una unidad: ").strip().upper()
        if eleccion_unidad == '0':
            print("Saliendo del programa.")
            break
        elif eleccion_unidad == 'H':
            mostrar_historial()

        elif eleccion_unidad == 'R':
            continue  # Refresca el menú
        elif eleccion_unidad in UNIDADES:
            ruta_unidad = os.path.join(RUTA_BASE, UNIDADES[eleccion_unidad])
            if not validar_ruta(ruta_unidad):
                print(f" No existe la carpeta: {UNIDADES[eleccion]}")
                pausar()
                continue
            mostrar_sub_menu(ruta_unidad)
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")
            pausar()

def mostrar_sub_menu(ruta_unidad):

    while True:
        limpiar_pantalla()
        print("=" * 50)
        print(f" MENÚ - {os.path.basename(ruta_unidad)}")
        print("=" * 50)
        sub_carpetas = [f.name for f in os.scandir(ruta_unidad) if f.is_dir()]
        if not sub_carpetas:
            print("\nSubmenú - Selecciona una subcarpeta")
            pausar()
            return

        # Imprime las subcarpetas
        for i, carpeta in enumerate(sub_carpetas, start=1):
            print(f"{i} - {carpeta}")
        print("\nR - Refrescar subcarpetas")
        print("9 - Volver al menú principal")
        print("0 - volver")

        eleccion = input("\nElige una subcarpeta: ").strip().upper()
        if eleccion == '0':
            return  # Regresar al menú principal
        elif eleccion == '9':
            return  # Regresar al menú principal
        elif eleccion == 'R':
            continue  # Refresca el submenú
        else:
            try:
                index = int(eleccion) - 1
                if 0 <= index < len(sub_carpetas):
                    ruta_sub = os.path.join(ruta_unidad, sub_carpetas[index])
                    mostrar_scripts(ruta_sub)
                else:
                    print("Opción no válida. Por favor, intenta de nuevo.")
                    pausar()
            except ValueError:
                print("Debes ingresar un número válido.")
                pausar()

def mostrar_scripts(ruta_sub_carpeta):

    while True:
        limpiar_pantalla()
        print("=" * 50)
        print(f"📜 SCRIPTS EN: {os.path.basename(ruta_sub_carpeta)}")
        print("=" * 50)

        scripts = [f.name for f in os.scandir(ruta_sub_carpeta)
                   if f.is_file() and f.name.endswith('.py')]
        if not scripts:
            print(" No hay scripts en esta carpeta.")
            pausar()
            return

        for i, script in enumerate(scripts, start=1):
            print(f"{i} - {script}")
        print("\nB - Buscar script por nombre")
        print("R - Refrescar lista de scripts")
        print("9 - Regresar al menú principal")
        print("0 - volver")

        eleccion = input("\nElige un script: ").strip().upper()
        if eleccion == '0':
            return
        elif eleccion == '9':
            return  # Regresar al menú principal
        elif eleccion == 'R':
            continue  # Refresca la lista de scripts
        elif eleccion == 'B':
            buscar_scripts(ruta_sub_carpeta)
            continue
        else:
            try:
                index = int(eleccion) - 1
                if 0 <= index < len(scripts):
                    ruta_script = os.path.join(ruta_sub_carpeta, scripts[index])
                    
                    limpiar_pantalla()
                    codigo = mostrar_codigo(ruta_script)
                    if codigo:
                        print("\n¿Qué deseas hacer?")
                        print("1 - Ejecutar el script")
                        print("2 - Abrir en VSCode")
                        print("0 - Regresar al menú de scripts")

                        opcion= input("\nElige una opción: ").strip()
                        if opcion == '1':
                            ejecutar_codigo(ruta_script)
                        elif opcion == '2':
                            abrir_en_vscode(ruta_script)
                        else:
                            print("Cancelado.")
                    pausar()
                else:
                    print("Opción no válida. Por favor, intenta de nuevo.")
                    pausar()
            except ValueError:
                print("Opción no válida. Por favor, intenta de nuevo.")
                pausar()
            

# Ejecutar el dashboard
if __name__ == "__main__":
    mostrar_menu()

