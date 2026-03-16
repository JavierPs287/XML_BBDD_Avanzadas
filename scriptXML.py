import xml.etree.ElementTree as ET

MIS_TEMAS = ["Food & Drink", "Travel", "Cars & Transportation", "Sports"]
ARCHIVO_ENTRADA = "FullOct2007.xml"
ARCHIVO_FILTRADO = "mis_categorias_yahoo.xml"

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
      <head><title>Visualización Yahoo Answers</title></head>
      <body>
        <h2 style="font-family: Arial;">Preguntas de mis Categorías</h2>
        <table border="1" style="border-collapse: collapse; font-family: Arial; width: 100%;">
          <tr bgcolor="#d3f4ff">
            <th style="padding: 8px;">Categoría</th>
            <th style="padding: 8px;">Subcategoría</th>
            <th style="padding: 8px;">Asunto (Subject)</th>
            <th style="padding: 8px;">Mejor Respuesta (Best Answer)</th>
          </tr>
          <xsl:for-each select="//vespaadd/document">
            <tr>
              <td style="padding: 8px;"><b><xsl:value-of select="maincat"/></b></td>
              <td style="padding: 8px;"><xsl:value-of select="subcat"/></td>
              <td style="padding: 8px;"><xsl:value-of select="subject"/></td>
              <td style="padding: 8px; color: green;"><xsl:value-of select="bestanswer"/></td>
            </tr>
          </xsl:for-each>
        </table>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>"""

    with open("esquema_proyecto.xsd", "w", encoding="utf-8") as f:
        f.write(xsd_content)
    with open("visualizador.xslt", "w", encoding="utf-8") as f:
        f.write(xslt_content)
    print("✓ Archivos XSD y XSLT generados correctamente.")

def filtrar_por_categorias(entrada, salida, temas):
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

if __name__ == "__main__":
    generar_archivos_soporte()
    # leer_temas(ARCHIVO_ENTRADA)
    filtrar_por_categorias(ARCHIVO_ENTRADA, ARCHIVO_FILTRADO, MIS_TEMAS)