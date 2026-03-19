import xml.etree.ElementTree as ET
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import argparse

MIS_TEMAS = ["Food & Drink", "Travel", "Cars & Transportation", "Sports"]
ARCHIVO_ENTRADA = "FullOct2007.xml"
ARCHIVO_FILTRADO = "mis_categorias_yahoo.xml"
# Para pruebas/demo
ARCHIVO_PREVIEW = "mis_categorias_preview.xml"
MAX_PREVIEW = 1000

def generar_archivos_soporte():
    """Genera los archivos XSD y XSLT basados en la estructura real del XML."""

    xsd_content = """<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="root">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="vespaadd" maxOccurs="unbounded">
          <xs:complexType>
            <xs:sequence>
              <xs:element name="document">
                <xs:complexType>
                  <xs:sequence>
                    <xs:element name="uri"         type="xs:string"/>
                    <xs:element name="subject"     type="xs:string"/>
                    <xs:element name="content"     type="xs:string" minOccurs="0"/>
                    <xs:element name="bestanswer"  type="xs:string"/>
                    <xs:element name="nbestanswers">
                      <xs:complexType>
                        <xs:sequence>
                          <xs:element name="answer_item" type="xs:string" maxOccurs="unbounded"/>
                        </xs:sequence>
                      </xs:complexType>
                    </xs:element>
                    <xs:element name="cat"         type="xs:string" minOccurs="0"/>
                    <xs:element name="maincat"     type="xs:string" minOccurs="0"/>
                    <xs:element name="subcat"      type="xs:string" minOccurs="0"/>
                    <xs:element name="date"        type="xs:string"/>
                    <xs:element name="res_date"    type="xs:string" minOccurs="0"/>
                    <xs:element name="vot_date"    type="xs:string" minOccurs="0"/>
                    <xs:element name="lastanswerts" type="xs:string"/>
                    <xs:element name="qlang"       type="xs:string" minOccurs="0"/>
                    <xs:element name="qintl"       type="xs:string" minOccurs="0"/>
                    <xs:element name="language"    type="xs:string" minOccurs="0"/>
                    <xs:element name="id"          type="xs:string"/>
                    <xs:element name="best_id"     type="xs:string" minOccurs="0"/>
                  </xs:sequence>
                  <xs:attribute name="type" type="xs:string"/>
                </xs:complexType>
              </xs:element>
            </xs:sequence>
          </xs:complexType>
        </xs:element>
      </xs:sequence>
    </xs:complexType>
  </xs:element>
</xs:schema>"""

    xslt_content = """<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:template match="/">
    <html>
      <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <title>Visualización Yahoo Answers</title>
        <style type="text/css">
          html, body {
            margin: 0;
            padding: 0;
            width: 100%;
            min-height: 100vh;
            font-family: Arial, sans-serif;
          }
          .wrap {
            box-sizing: border-box;
            width: 100%;
            padding: 16px;
          }
          .table-wrap {
            width: 100%;
            overflow-x: auto;
          }
          table {
            width: 100%;
            border-collapse: collapse;
            table-layout: fixed;
          }
          th, td {
            border: 1px solid #cfd8dc;
            padding: 8px;
            vertical-align: top;
            word-wrap: break-word;
          }
          th {
            background: #d3f4ff;
          }
          .answer {
            color: #1f7a1f;
          }
        </style>
      </head>
      <body>
        <div class="wrap">
          <h2>Preguntas de mis Categorías</h2>
          <div class="table-wrap">
            <table>
              <tr>
                <th>Categoría</th>
                <th>Subcategoría</th>
                <th>Asunto (Subject)</th>
                <th>Mejor Respuesta (Best Answer)</th>
              </tr>
              <xsl:for-each select="/root/vespaadd/document">
                <tr>
                  <td><b><xsl:value-of select="maincat"/></b></td>
                  <td><xsl:value-of select="subcat"/></td>
                  <td><xsl:value-of select="subject"/></td>
                  <td class="answer"><xsl:value-of select="bestanswer" disable-output-escaping="yes"/></td>
                </tr>
              </xsl:for-each>
            </table>
          </div>
        </div>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>"""

    with open("esquema_proyecto.xsd", "w", encoding="utf-8") as f:
        f.write(xsd_content)
    with open("visualizador.xslt", "w", encoding="utf-8") as f:
        f.write(xslt_content)
    print("✓ Archivos XSD y XSLT generados correctamente.")

def filtrar_por_categorias(entrada, salida, temas, max_registros=None):
    """Procesa el archivo de 12GB de forma iterativa para no agotar la RAM."""
    print(f"Iniciando filtrado de categorías: {temas}...")

    contador = 0
    try:
        with open(salida, "w", encoding="utf-8") as f_out:
            f_out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f_out.write('<?xml-stylesheet type="text/xsl" href="visualizador.xslt"?>\n')
            f_out.write("<root>\n")

            context = ET.iterparse(entrada, events=("end",))

            for event, elem in context:
                if elem.tag == "vespaadd":
                    maincat = elem.findtext("document/maincat")

                    if maincat in temas:
                        f_out.write(ET.tostring(elem, encoding="unicode") + "\n")
                        contador += 1
                        if contador % 10000 == 0:
                            print(f"  Extraídas {contador:,} preguntas...")
                        if max_registros is not None and contador >= max_registros:
                          break

                    elem.clear()

            f_out.write("</root>")
        print(f"✓ Proceso completado. Se han extraído {contador:,} preguntas en '{salida}'.")
    except FileNotFoundError:
        print(f"Error: No se encuentra el archivo '{entrada}'.")

def leer_temas(archivo):
    """Lee el archivo XML de forma iterativa y muestra los distintos temas (maincat)."""
    temas = set()
    contador = 0
    context = ET.iterparse(archivo, events=("end",))

    for event, elem in context:
        if elem.tag == "vespaadd":
            maincat = elem.findtext("document/maincat")
            if maincat:
                temas.add(maincat)
            contador += 1
            if contador % 100000 == 0:
                print(f"  Procesados {contador:,} registros...")
            elem.clear()

    print(f"Se encontraron {len(temas)} temas distintos:")
    for tema in sorted(temas):
        print(f"  - {tema}")

def conectar_mongodb():
    """Conecta a MongoDB usando variables de entorno (como hacías con MySQL) o local por defecto."""
    try:
        uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
        client = MongoClient(uri)
        db = client[os.getenv('DB_NAME', 'yahoo_answers')]
        print("✓ Conexión exitosa a MongoDB.")
        return db
    except Exception as e:
        print(f"Error al conectar a MongoDB: {e}")
        return None

def cargar_xml_a_mongodb(archivo_xml, db, chunk_size=5000):
    """Parsea iterativamente el XML y lo carga a MongoDB en lotes."""
    print(f"Iniciando carga a MongoDB desde '{archivo_xml}'...")
    
    coleccion = db['preguntas']  # Seleccionamos la colección (equivalente a la tabla)
    preguntas_batch = []
    contador = 0
    
    try:
        context = ET.iterparse(archivo_xml, events=("end",))
        for event, elem in context:
            if elem.tag == "vespaadd":
                doc = elem.find("document")
                if doc is not None:
                    
                    pregunta = {
                        "id_usuario_pregunta": doc.findtext("id"),          
                        "id_usuario_mejor_respuesta": doc.findtext("best_id"), 
                        "uri_pregunta": doc.findtext("uri"),                
                        "subject": doc.findtext("subject"),
                        "content": doc.findtext("content"),
                        "bestanswer": doc.findtext("bestanswer"),
                        "cat": doc.findtext("cat"),
                        "maincat": doc.findtext("maincat"),
                        "subcat": doc.findtext("subcat"),
                        
                        # Convertimos las fechas a enteros (int) para poder hacer < o > en MongoDB
                        "date": int(doc.findtext("date")) if doc.findtext("date") else None,
                        "res_date": int(doc.findtext("res_date")) if doc.findtext("res_date") else None,
                        
                        "lastanswerts": doc.findtext("lastanswerts"),
                        "otras_respuestas": [] # Array para embeber las respuestas (Diseño Documental)
                    }
                    # ----------------------------------------------------
                    
                    # Extraer respuestas alternativas e insertarlas en la misma pregunta
                    nbestanswers = doc.find("nbestanswers")
                    if nbestanswers is not None:
                        for answer in nbestanswers.findall("answer_item"):
                            if answer.text:
                                pregunta["otras_respuestas"].append(answer.text)
                    
                    preguntas_batch.append(pregunta)
                    contador += 1
                    
                    # Volcar el lote a la base de datos para salvar RAM (usando insert_many)
                    if contador % chunk_size == 0:
                        coleccion.insert_many(preguntas_batch)
                        preguntas_batch = []
                        print(f"  Insertados {contador:,} registros a MongoDB...")
                
                elem.clear() # Liberar memoria
        
        # Insertar los registros restantes que quedaron en el buffer
        if preguntas_batch:
            coleccion.insert_many(preguntas_batch)
            
        print(f"✓ Carga finalizada con éxito en MongoDB. Total de preguntas extraídas: {contador:,}")
        
    except ET.ParseError as e:
        print(f"Error parseando el archivo XML: {e}")
    except FileNotFoundError:
        print(f"Error: El archivo '{archivo_xml}' no existe.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Procesa Yahoo Answers en modo demo o final.")
    parser.add_argument(
        "--modo",
        choices=["demo", "final"],
        default="demo",
        help="demo: genera un XML pequeño para visualizar. final: genera XML completo y carga en MongoDB."
    )
    args = parser.parse_args()

    load_dotenv()
    generar_archivos_soporte()

    if args.modo == "demo":
        print(f"Modo demo: generando vista previa con {MAX_PREVIEW} registros...")
        filtrar_por_categorias(
            ARCHIVO_ENTRADA,
            ARCHIVO_PREVIEW,
            MIS_TEMAS,
            max_registros=MAX_PREVIEW
        )
        print(f"Abre '{ARCHIVO_PREVIEW}' en el navegador con el servidor HTTP.")
    else:
        print("Modo final: generando XML completo y cargando en MongoDB...")
        filtrar_por_categorias(ARCHIVO_ENTRADA, ARCHIVO_FILTRADO, MIS_TEMAS)

        db = conectar_mongodb()
        if db is not None:
            db.drop_collection('preguntas')  # Limpiar la colección antes de cargar nuevos datos
            cargar_xml_a_mongodb(ARCHIVO_FILTRADO, db)