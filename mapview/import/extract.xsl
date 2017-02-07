<?xml version="1.0" ?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:variable name="class-full-text" select="//h2"/>
  <xsl:variable name="class" select="normalize-space(substring-after($class-full-text, ':'))"/>


  <xsl:template match="/">
    <xsl:apply-templates select=".//table[@id='listeEtudiants']" />
  </xsl:template>

  <xsl:template match="table[@id='listeEtudiants']">
    <xsl:for-each select="tbody/tr">
    <student>
      <firstname><xsl:value-of select="td[3]"/></firstname>
      <lastname><xsl:value-of select="td[2]"/></lastname>
      <email><xsl:value-of select="td[4]"/></email>
      <fc><xsl:value-of select='boolean(./@class="formationContinue")'/></fc>
      <class><xsl:value-of select="$class" /></class>
    </student>
    </xsl:for-each>
  </xsl:template>

</xsl:stylesheet>
