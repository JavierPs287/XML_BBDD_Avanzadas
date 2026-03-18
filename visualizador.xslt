<?xml version="1.0" encoding="UTF-8"?>
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
</xsl:stylesheet>