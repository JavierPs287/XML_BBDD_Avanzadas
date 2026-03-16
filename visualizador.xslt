<?xml version="1.0" encoding="UTF-8"?>
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
</xsl:stylesheet>