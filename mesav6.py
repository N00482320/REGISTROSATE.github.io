import os
from datetime import datetime

# Códigos de color ANSI para la consola
ROJO = "\033[91m"
VERDE = "\033[92m"
AMARILLO = "\033[93m"
AZUL = "\033[94m"
RESET = "\033[0m"

# Archivo de persistencia de datos
NOMBRE_ARCHIVO = "expedientes_mesa_de_partes.txt"

def cargar_datos():
    """Carga los expedientes guardados previamente en el archivo plano."""
    expedientes = []
    if os.path.exists(NOMBRE_ARCHIVO):
        try:
            with open(NOMBRE_ARCHIVO, "r", encoding="utf-8") as f:
                for linea in f:
                    partes = linea.strip().split("|")
                    # Compatibilidad con versiones anteriores y la nueva estructura completa (9 campos)
                    if len(partes) == 4:
                        expedientes.append({
                            "codigo": partes[0],
                            "documento": partes[1],
                            "remitente": partes[2],
                            "asunto": partes[3],
                            "fecha": "26/10/2026 00:00",
                            "estado": "PENDIENTE",
                            "tipo": "General",
                            "area": "Secretaría General",
                            "observaciones": "Ninguna"
                        })
                    elif len(partes) == 6:
                        expedientes.append({
                            "codigo": partes[0],
                            "documento": partes[1],
                            "remitente": partes[2],
                            "asunto": partes[3],
                            "fecha": partes[4],
                            "estado": partes[5],
                            "tipo": "General",
                            "area": "Secretaría General",
                            "observaciones": "Ninguna"
                        })
                    elif len(partes) == 9:
                        expedientes.append({
                            "codigo": partes[0],
                            "documento": partes[1],
                            "remitente": partes[2],
                            "asunto": partes[3],
                            "fecha": partes[4],
                            "estado": partes[5],
                            "tipo": partes[6],
                            "area": partes[7],
                            "observaciones": partes[8]
                        })
        except Exception as e:
            print(f"{ROJO}[ERROR] No se pudo leer el archivo: {e}{RESET}")
    return expedientes

def guardar_datos(expedientes):
    """Guarda la lista actualizada de expedientes en el archivo plano."""
    try:
        with open(NOMBRE_ARCHIVO, "w", encoding="utf-8") as f:
            for exp in expedientes:
                f.write(f"{exp['codigo']}|{exp['documento']}|{exp['remitente']}|{exp['asunto']}|{exp['fecha']}|{exp['estado']}|{exp['tipo']}|{exp['area']}|{exp['observaciones']}\n")
        print(f"\n{VERDE}[ÉXITO] Datos guardados permanentemente en el archivo.{RESET}")
    except Exception as e:
        print(f"{ROJO}[ERROR] Ocurrió un fallo al guardar los datos: {e}{RESET}")

def validar_documento(doc):
    """Valida si el DNI (8 dígitos) o RUC (11 dígitos) contiene solo números."""
    doc_limpio = doc.strip()
    return doc_limpio.isdigit() and len(doc_limpio) in (8, 11)

def formatear_celda(texto, ancho):
    """Ajusta el texto exactamente al ancho de la celda, recortando si es muy largo."""
    texto_str = str(texto)
    if len(texto_str) > ancho:
        return texto_str[:ancho-2] + ".."
    return f"{texto_str:<{ancho}}"

def generar_comprobante(exp):
    """Genera un archivo de texto individual como cargo de recepción digital."""
    nombre_txt = f"Comprobante_{exp['codigo']}.txt"
    try:
        with open(nombre_txt, "w", encoding="utf-8") as f:
            f.write("========================================\n")
            f.write("   MUNICIPALIDAD DE LIMA NORTE - TICKET\n")
            f.write("      COMPROBANTE DE MESA DE PARTES\n")
            f.write("========================================\n")
            f.write(f"CÓDIGO      : {exp['codigo']}\n")
            f.write(f"FECHA/HORA  : {exp['fecha']}\n")
            f.write(f"TIPO TRÁMITE: {exp['tipo']}\n")
            f.write(f"ÁREA DESTINO: {exp['area']}\n")
            f.write(f"DNI/RUC     : {exp['documento']}\n")
            f.write(f"REMITENTE   : {exp['remitente']}\n")
            f.write(f"ASUNTO      : {exp['asunto']}\n")
            f.write(f"ESTADO      : {exp['estado']}\n")
            f.write(f"OBSERVACIONES: {exp['observaciones']}\n")
            f.write("========================================\n")
            f.write("Guarde este código para consultar el estado.\n")
        print(f"{VERDE}[COMPROBANTE] Se generó el archivo '{nombre_txt}' exitosamente.{RESET}")
    except Exception as e:
        print(f"{ROJO}[ERROR] No se pudo generar el comprobante TXT: {e}{RESET}")

def registrar_expediente(expedientes):
    """Captura y valida la información del expediente incluyendo tipo y área de derivación."""
    print(f"\n{AMARILLO}--- REGISTRO DE NUEVO EXPEDIENTE ---{RESET}")
    
    num_correlativo = len(expedientes) + 1
    codigo = f"EXP-2026-{num_correlativo:04d}"
    print(f"{AZUL}Código asignado:{RESET} {codigo}")
    
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
    print(f"{AZUL}Fecha y Hora de registro:{RESET} {fecha_actual}")
    
    while True:
        doc = input("Ingrese DNI (8 dígitos) o RUC (11 dígitos) del remitente: ").strip()
        if validar_documento(doc):
            break
        print(f"{ROJO}[ATENCIÓN] El documento ingresado no es válido. Debe escribir un DNI (8 dígitos) o RUC (11 dígitos) numéricos.{RESET}")
        
    remitente = input("Ingrese Nombre Completo o Razón Social: ").strip()
    while not remitente:
        remitente = input(f"{ROJO}[OBLIGATORIO] El nombre no puede estar vacío:{RESET} ").strip()
        
    # Módulo de Tipos de Trámite Institucional
    print("\nSeleccione el Tipo de Trámite:")
    print("  1. Licencia de Funcionamiento")
    print("  2. Reclamo / Queja")
    print("  3. Solicitud de Obras")
    print("  4. Constancia de Posesión")
    print("  5. Otro / General")
    t_op = input("Seleccione opción (1-5): ").strip()
    tipos_map = {
        "1": "Licencia de Funcionamiento",
        "2": "Reclamo",
        "3": "Solicitud de Obras",
        "4": "Constancia de Posesión",
        "5": "General"
    }
    tipo_tramite = tipos_map.get(t_op, "General")

    # Módulo de Derivación de Oficinas / Áreas
    print("\nSeleccione el Área de Destino (Derivación):")
    print("  1. Gerencia de Rentas")
    print("  2. Obras Públicas")
    print("  3. Secretaría General")
    print("  4. Desarrollo Social")
    a_op = input("Seleccione opción (1-4): ").strip()
    areas_map = {
        "1": "Gerencia de Rentas",
        "2": "Obras Públicas",
        "3": "Secretaría General",
        "4": "Desarrollo Social"
    }
    area_destino = areas_map.get(a_op, "Secretaría General")

    asunto = input("Ingrese el Asunto/Detalle del trámite: ").strip()
    while not asunto:
        asunto = input(f"{ROJO}[OBLIGATORIO] El asunto no puede estar vacío:{RESET} ").strip()
        
    observaciones = input("Ingrese observaciones iniciales o notas (opcional): ").strip()
    if not observaciones:
        observaciones = "Ninguna"
        
    nuevo = {
        "codigo": codigo,
        "documento": doc,
        "remitente": remitente,
        "asunto": asunto,
        "fecha": fecha_actual,
        "estado": "PENDIENTE",
        "tipo": tipo_tramite,
        "area": area_destino,
        "observaciones": observaciones
    }
    
    expedientes.append(nuevo)
    print(f"\n{VERDE}[CONFIRMACIÓN] Expediente {codigo} registrado con éxito y derivado a {area_destino}.{RESET}")
    generar_comprobante(nuevo)

def buscar_expediente(expedientes):
    """Búsqueda lineal por código exacto de expediente."""
    print(f"\n{AMARILLO}--- BÚSQUEDA DE EXPEDIENTE POR CÓDIGO ---{RESET}")
    cod_buscar = input("Ingrese el código a buscar (ej. EXP-2026-0001): ").strip().upper()
    
    hallado = False
    for exp in expedientes:
        if exp["codigo"].upper() == cod_buscar:
            print(f"\n{AZUL}----------------------------------------{RESET}")
            print(f"CÓDIGO      : {exp['codigo']}")
            print(f"FECHA       : {exp['fecha']}")
            print(f"TIPO        : {exp['tipo']}")
            print(f"ÁREA        : {exp['area']}")
            print(f"DNI/RUC     : {exp['documento']}")
            print(f"REMITENTE   : {exp['remitente']}")
            print(f"ASUNTO      : {exp['asunto']}")
            print(f"ESTADO      : {exp['estado']}")
            print(f"OBSERVACIONES: {exp['observaciones']}")
            print(f"{AZUL}----------------------------------------{RESET}")
            hallado = True
            break
            
    if not hallado:
        print(f"\n{ROJO}[INFORMACIÓN] No se encontró ningún expediente con el código '{cod_buscar}'.{RESET}")

def busqueda_avanzada(expedientes):
    """Permite filtrar por número de documento o por coincidencia parcial en el nombre del remitente."""
    print(f"\n{AMARILLO}--- BÚSQUEDA AVANZADA / FILTRADO ---{RESET}")
    if not expedientes:
        print(f"{ROJO}No hay expedientes registrados en el sistema.{RESET}")
        return

    print("1. Buscar por número de DNI o RUC")
    print("2. Buscar por nombre o coincidencia de Remitente")
    op = input("Seleccione criterio de búsqueda (1-2): ").strip()

    resultados = []
    if op == "1":
        doc_buscado = input("Ingrese el DNI o RUC a buscar: ").strip()
        resultados = [e for e in expedientes if doc_buscado in e["documento"]]
    elif op == "2":
        nombre_buscado = input("Ingrese parte del nombre o razón social: ").strip().lower()
        resultados = [e for e in expedientes if nombre_buscado in e["remitente"].lower()]
    else:
        print(f"{ROJO}[ERROR] Opción no válida.{RESET}")
        return

    if not resultados:
        print(f"\n{ROJO}[INFORMACIÓN] No se encontraron expedientes con ese criterio.{RESET}")
        return

    print(f"\n{VERDE}Se encontraron {len(resultados)} coincidencia(s):{RESET}")
    col_widths = [12, 14, 18, 18, 20, 12]
    print(f"{VERDE}┌" + "┬".join("─" * (w + 2) for w in col_widths) + f"┐{RESET}")
    headers = ["CÓDIGO", "TIPO", "REMITENTE", "ÁREA", "ASUNTO", "ESTADO"]
    print(f"{VERDE}│{RESET} " + f" {VERDE}│{RESET} ".join(formatear_celda(h, w) for h, w in zip(headers, col_widths)) + f" {VERDE}│{RESET}")
    print(f"{VERDE}├" + "┼".join("─" * (w + 2) for w in col_widths) + f"┤{RESET}")
    
    for idx, exp in enumerate(resultados):
        valores = [exp['codigo'], exp['tipo'], exp['remitente'], exp['area'], exp['asunto'], exp['estado']]
        print(f"{VERDE}│{RESET} " + f" {VERDE}│{RESET} ".join(formatear_celda(v, w) for v, w in zip(valores, col_widths)) + f" {VERDE}│{RESET}")
        if idx < len(resultados) - 1:
            print(f"{VERDE}├" + "┼".join("─" * (w + 2) for w in col_widths) + f"┤{RESET}")
    print(f"{VERDE}└" + "┴".join("─" * (w + 2) for w in col_widths) + f"┘{RESET}")

def ordenar_y_listar(expedientes):
    """Ordena los expedientes mediante Bubble Sort y los muestra en una tabla tipo Excel con recuadro verde."""
    print(f"\n{AMARILLO}--- LISTADO DE EXPEDIENTES REGISTRADOS ---{RESET}")
    if not expedientes:
        print(f"{VERDE}┌──────────────────────────────────────────────┐{RESET}")
        print(f"{VERDE}│{RESET} {ROJO}No hay expedientes registrados en el sistema.{RESET}          {VERDE}│{RESET}")
        print(f"{VERDE}└──────────────────────────────────────────────┘{RESET}")
        return
        
    n = len(expedientes)
    for i in range(n):
        for j in range(0, n - i - 1):
            if expedientes[j]["codigo"] > expedientes[j + 1]["codigo"]:
                expedientes[j], expedientes[j + 1] = expedientes[j + 1], expedientes[j]
                
    col_widths = [12, 14, 18, 18, 20, 12]
    print(f"{VERDE}┌" + "┬".join("─" * (w + 2) for w in col_widths) + f"┐{RESET}")
    headers = ["CÓDIGO", "TIPO", "REMITENTE", "ÁREA", "ASUNTO", "ESTADO"]
    print(f"{VERDE}│{RESET} " + f" {VERDE}│{RESET} ".join(formatear_celda(h, w) for h, w in zip(headers, col_widths)) + f" {VERDE}│{RESET}")
    print(f"{VERDE}├" + "┼".join("─" * (w + 2) for w in col_widths) + f"┤{RESET}")
    
    for idx, exp in enumerate(expedientes):
        valores = [exp['codigo'], exp['tipo'], exp['remitente'], exp['area'], exp['asunto'], exp['estado']]
        print(f"{VERDE}│{RESET} " + f" {VERDE}│{RESET} ".join(formatear_celda(v, w) for v, w in zip(valores, col_widths)) + f" {VERDE}│{RESET}")
        if idx < len(expedientes) - 1:
            print(f"{VERDE}├" + "┼".join("─" * (w + 2) for w in col_widths) + f"┤{RESET}")
    print(f"{VERDE}└" + "┴".join("─" * (w + 2) for w in col_widths) + f"┘{RESET}")

def modificar_expediente(expedientes):
    """Permite corregir remitente, asunto, estado o agregar observaciones al buzón."""
    print(f"\n{AMARILLO}--- MODIFICAR / ACTUALIZAR EXPEDIENTE ---{RESET}")
    if not expedientes:
        print(f"{ROJO}No hay expedientes en el sistema para modificar.{RESET}")
        return

    cod = input("Ingrese el código del expediente a modificar (ej. EXP-2026-0001): ").strip().upper()
    encontrado = None
    for exp in expedientes:
        if exp["codigo"].upper() == cod:
            encontrado = exp
            break

    if not encontrado:
        print(f"{ROJO}[ERROR] No se encontró el expediente con código '{cod}'.{RESET}")
        return

    print(f"\nExpediente encontrado: {encontrado['codigo']} | Estado actual: {encontrado['estado']}")
    print("1. Modificar Remitente")
    print("2. Modificar Asunto")
    print("3. Actualizar Estado del Trámite (Workflow)")
    print("4. Agregar / Actualizar Buzón de Observaciones")
    op = input("Seleccione qué desea hacer (1-4): ").strip()

    if op == "1":
        nuevo_rem = input("Ingrese el nuevo Remitente / Razón Social: ").strip()
        if nuevo_rem:
            encontrado["remitente"] = nuevo_rem
            print(f"\n{VERDE}[ÉXITO] Remitente actualizado.{RESET}")
    elif op == "2":
        nuevo_asu = input("Ingrese el nuevo Asunto: ").strip()
        if nuevo_asu:
            encontrado["asunto"] = nuevo_asu
            print(f"\n{VERDE}[ÉXITO] Asunto actualizado.{RESET}")
    elif op == "3":
        print("\nSeleccione el nuevo estado:")
        print("  1. PENDIENTE")
        print("  2. EN REVISIÓN")
        print("  3. APROBADO")
        print("  4. RECHAZADO (Subsanación)")
        est_op = input("Opción de estado (1-4): ").strip()
        estados_map = {"1": "PENDIENTE", "2": "EN REVISIÓN", "3": "APROBADO", "4": "RECHAZADO"}
        if est_op in estados_map:
            encontrado["estado"] = estados_map[est_op]
            print(f"\n{VERDE}[ÉXITO] Estado del trámite actualizado a: {encontrado['estado']}{RESET}")
        else:
            print(f"{ROJO}[ERROR] Opción de estado no válida.{RESET}")
    elif op == "4":
        nueva_obs = input("Ingrese la nota u observación para el ciudadano: ").strip()
        if nueva_obs:
            encontrado["observaciones"] = nueva_obs
            print(f"\n{VERDE}[ÉXITO] Observación registrada en el buzón.{RESET}")
    else:
        print(f"{ROJO}[ERROR] Opción no válida.{RESET}")

def eliminar_expediente(expedientes):
    """Da de baja/elimina un expediente mediante su código con confirmación."""
    print(f"\n{AMARILLO}--- ELIMINAR EXPEDIENTE ---{RESET}")
    if not expedientes:
        print(f"{ROJO}No hay expedientes en el sistema para eliminar.{RESET}")
        return

    cod = input("Ingrese el código del expediente a eliminar (ej. EXP-2026-0001): ").strip().upper()
    encontrado = None
    for exp in expedientes:
        if exp["codigo"].upper() == cod:
            encontrado = exp
            break

    if not encontrado:
        print(f"{ROJO}[ERROR] No se encontró el expediente con código '{cod}'.{RESET}")
        return

    print(f"\nSe va a eliminar el expediente:")
    print(f"Código: {encontrado['codigo']} | Remitente: {encontrado['remitente']} | Asunto: {encontrado['asunto']}")
    confirmacion = input(f"{ROJO}¿Está seguro de eliminar este expediente? (S/N): {RESET}").strip().upper()

    if confirmacion == "S":
        expedientes.remove(encontrado)
        print(f"\n{VERDE}[ÉXITO] El expediente {cod} ha sido eliminado del sistema.{RESET}")
    else:
        print(f"{AMARILLO}[CANCELADO] La operación de eliminación fue cancelada.{RESET}")

def exportar_csv(expedientes):
    """Exporta los expedientes actuales a un archivo CSV compatible con Excel."""
    print(f"\n{AMARILLO}--- EXPORTAR DATOS A CSV ---{RESET}")
    if not expedientes:
        print(f"{ROJO}No hay expedientes para exportar.{RESET}")
        return
    
    nombre_csv = "reporte_expedientes.csv"
    try:
        with open(nombre_csv, "w", encoding="utf-8-sig") as f:
            f.write("Codigo,FechaHora,Tipo,Area,Documento,Remitente,Asunto,Estado,Observaciones\n")
            for exp in expedientes:
                f.write(f"{exp['codigo']},{exp['fecha']},{exp['tipo']},{exp['area']},{exp['documento'],},\"{exp['remitente']}\",\"{exp['asunto']}\",{exp['estado']},\"{exp['observaciones']}\"\n")
        print(f"{VERDE}[ÉXITO] Datos exportados correctamente al archivo '{nombre_csv}'. ¡Ya puedes abrirlo en Excel!{RESET}")
    except Exception as e:
        print(f"{ROJO}[ERROR] No se pudo exportar el archivo CSV: {e}{RESET}")

def hacer_backup(expedientes):
    """Genera una copia de respaldo exacta de la base de datos."""
    print(f"\n{AMARILLO}--- SISTEMA DE COPIA DE SEGURIDAD (BACKUP) ---{RESET}")
    if not expedientes:
        print(f"{ROJO}No hay datos para respaldar.{RESET}")
        return
        
    nombre_backup = "respaldo_expedientes.txt"
    try:
        with open(nombre_backup, "w", encoding="utf-8") as f:
            for exp in expedientes:
                f.write(f"{exp['codigo']}|{exp['documento']}|{exp['remitente']}|{exp['asunto']}|{exp['fecha']}|{exp['estado']}|{exp['tipo']}|{exp['area']}|{exp['observaciones']}\n")
        print(f"{VERDE}[ÉXITO] Copia de seguridad generada correctamente en '{nombre_backup}'.{RESET}")
    except Exception as e:
        print(f"{ROJO}[ERROR] Ocurrió un fallo al crear el respaldo: {e}{RESET}")

def mostrar_estadisticas(expedientes):
    """Muestra información analítica del sistema incluyendo gráficos de barras ASCII."""
    print(f"\n{AZUL}==========================================")
    print("       ESTADÍSTICAS DEL SISTEMA")
    print(f"=========================================={RESET}")
    
    total = len(expedientes)
    if total == 0:
        print(f"{ROJO}No hay datos suficientes para generar estadísticas.{RESET}")
        return

    dni_count = sum(1 for e in expedientes if len(e["documento"]) == 8)
    ruc_count = sum(1 for e in expedientes if len(e["documento"]) == 11)
    pendientes = sum(1 for e in expedientes if e["estado"] == "PENDIENTE")
    en_revision = sum(1 for e in expedientes if e["estado"] == "EN REVISIÓN")
    aprobados = sum(1 for e in expedientes if e["estado"] == "APROBADO")
    rechazados = sum(1 for e in expedientes if e["estado"] == "RECHAZADO")
    ultimo_codigo = expedientes[-1]["codigo"] if expedientes else "Ninguno"

    print(f"• Total de expedientes registrados : {total}")
    print(f"• Trámites con DNI (Personas Nat.)  : {dni_count}")
    print(f"• Trámites con RUC (Empresas)      : {ruc_count}")
    print(f"• Último código generado           : {ultimo_codigo}\n")

    print(f"{AMARILLO}--- GRÁFICO ESTADÍSTICO (ESTADOS) ---{RESET}")
    print(f"PENDIENTES  : {'█' * pendientes} ({pendientes})")
    print(f"EN REVISIÓN : {'█' * en_revision} ({en_revision})")
    print(f"APROBADOS   : {'█' * aprobados} ({aprobados})")
    print(f"RECHAZADOS  : {'█' * rechazados} ({rechazados})")
    print(f"{AZUL}=========================================={RESET}")

def mostrar_ayuda_faq():
    """Muestra el manual de usuario y preguntas frecuentes (FAQ)."""
    print(f"\n{AZUL}==========================================")
    print("         MENÚ DE AYUDA / FAQ")
    print(f"=========================================={RESET}")
    print("1. ¿Cómo se genera el código de expediente?")
    print("   -> Se genera automáticamente de forma correlativa (Ej. EXP-2026-0001).")
    print("2. ¿Qué documentos son válidos para el remitente?")
    print("   -> DNI de exactamente 8 dígitos numéricos o RUC de 11 dígitos numéricos.")
    print("3. ¿Para qué sirve el buzón de observaciones?")
    print("   -> Permite dejar notas internas o requerir la subsanación de documentos al ciudadano.")
    print("4. ¿Dónde se guardan los datos?")
    print("   -> En el archivo plano 'expedientes_mesa_de_partes.txt' ubicado en tu misma carpeta.")
    print(f"{AZUL}=========================================={RESET}")

def login_sistema():
    """Sistema básico de roles y permisos por consola."""
    print(f"\n{AZUL}==========================================")
    print("    CONTROL DE ACCESO - MUNI LIMA NORTE")
    print(f"=========================================={RESET}")
    print("Seleccione su perfil de usuario:")
    print("  1. Administrador (Control total del sistema)")
    print("  2. Personal de Mesa de Partes (Registro y gestión)")
    print("  3. Ciudadano / Consulta (Solo lectura y búsqueda)")
    
    rol_op = input("Seleccione perfil (1-3): ").strip()
    if rol_op == "1":
        print(f"{VERDE}[ACCESO CONCEDIDO] Perfil: Administrador{RESET}")
        return "ADMIN"
    elif rol_op == "2":
        print(f"{VERDE}[ACCESO CONCEDIDO] Perfil: Personal de Mesa de Partes{RESET}")
        return "PERSONAL"
    elif rol_op == "3":
        print(f"{VERDE}[ACCESO CONCEDIDO] Perfil: Ciudadano / Consulta{RESET}")
        return "CIUDADANO"
    else:
        print(f"{ROJO}[ACCESO DÉBIL/INVÁLIDO] Ingresando por defecto como Personal.{RESET}")
        return "PERSONAL"

def main():
    rol_actual = login_sistema()
    expedientes = cargar_datos()
    
    while True:
        print(f"\n{AZUL}==========================================")
        print(f" MESA DE PARTES DIGITAL - PERFIL: [{rol_actual}]")
        print(f"=========================================={RESET}")
        
        # Menú dinámico según los permisos del rol
        if rol_actual in ("ADMIN", "PERSONAL"):
            print("1. Registrar nuevo expediente")
            print("2. Buscar expediente por código")
            print("3. Búsqueda avanzada / Filtrado")
            print("4. Ordenar y listar expedientes")
            print("5. Modificar expediente / Actualizar Estado / Buzón")
            if rol_actual == "ADMIN":
                print("6. Eliminar expediente")
            print("7. Estadísticas y Gráficos del Sistema")
            print("8. Exportar datos a formato CSV (Excel)")
            print("9. Generar Copia de Seguridad (Backup)")
            print("10. Menú de Ayuda / FAQ")
            print("11. Guardar cambios y salir")
        else:
            # Menú limitado para el Ciudadano
            print("2. Buscar expediente por código")
            print("3. Búsqueda avanzada / Filtrado")
            print("4. Ordenar y listar expedientes")
            print("10. Menú de Ayuda / FAQ")
            print("11. Salir del sistema")
        
        opcion = input("Seleccione una opción: ").strip()
        
        if rol_actual in ("ADMIN", "PERSONAL"):
            if opcion == "1":
                registrar_expediente(expedientes)
            elif opcion == "2":
                buscar_expediente(expedientes)
            elif opcion == "3":
                busqueda_avanzada(expedientes)
            elif opcion == "4":
                ordenar_y_listar(expedientes)
            elif opcion == "5":
                modificar_expediente(expedientes)
            elif opcion == "6" and rol_actual == "ADMIN":
                eliminar_expediente(expedientes)
            elif opcion == "6" and rol_actual != "ADMIN":
                print(f"{ROJO}[ACCESO DENEGADO] Solo el Administrador puede eliminar registros.{RESET}")
            elif opcion == "7":
                mostrar_estadisticas(expedientes)
            elif opcion == "8":
                exportar_csv(expedientes)
            elif opcion == "9":
                hacer_backup(expedientes)
            elif opcion == "10":
                mostrar_ayuda_faq()
            elif opcion == "11":
                guardar_datos(expedientes)
                print(f"{VERDE}Gracias por utilizar el prototipo de Mesa de Partes Digital.{RESET}")
                break
            else:
                print(f"{ROJO}[ERROR] Opción no válida o sin permisos.{RESET}")
        else:
            # Lógica para Ciudadano
            if opcion == "2":
                buscar_expediente(expedientes)
            elif opcion == "3":
                busqueda_avanzada(expedientes)
            elif opcion == "4":
                ordenar_y_listar(expedientes)
            elif opcion == "10":
                mostrar_ayuda_faq()
            elif opcion == "11":
                print(f"{VERDE}Gracias por consultar el sistema de Mesa de Partes Digital.{RESET}")
                break
            else:
                print(f"{ROJO}[ERROR] Opción no válida para su perfil.{RESET}")

if __name__ == "__main__":
    main()