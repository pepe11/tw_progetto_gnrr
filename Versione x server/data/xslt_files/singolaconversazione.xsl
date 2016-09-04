<?xml version="1.0" encoding="utf-8"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:ts="http://www.dominio.com">
  <!--<xsl:output method='html' version='1.0' encoding='UTF-8' indent='yes' doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd" doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN" omit-xml-declaration="yes"/> -->


  <xsl:template match="/">


    <h1>Conversazione con
    <a>
      <xsl:attribute name="href">profilo.cgi?utente=[% UTENTE %]</xsl:attribute>
      <xsl:attribute name="tabindex">10</xsl:attribute>
      [% UTENTE %]
    </a>
    </h1>

    <xsl:for-each select="ts:TravelShare/SetMessaggi/Conversazione[@User1='[% UTENTE %]' and @User2='[% MYSELF %]']/Messaggio | ts:TravelShare/SetMessaggi/Conversazione[@User1='[% MYSELF %]' and @User2='[% UTENTE %]']/Messaggio"> <!-- FILTRI PERL 'u1' 'u2' -->
      <xsl:choose>
        <xsl:when test=" Mittente ='[% MYSELF %]'  ">
          <div class="inviati" >
            <p class="intestazioneMsg"><xsl:call-template name="formatdate"><xsl:with-param name="datestr" select="Data" /></xsl:call-template>  - <xsl:value-of select="Ora"/></p>
            <p><xsl:value-of select="Testo"/></p>
          </div>
        </xsl:when>
        <xsl:otherwise>
          <div class="ricevuti" >  <!-- DIVISIONE FRA LETTI E NON LETTI -->
            <xsl:if test="@Letto = 'no'">
              <p>NUOVO MESSAGGIO</p>
            </xsl:if>
            <p class="intestazioneMsg"><xsl:call-template name="formatdate"><xsl:with-param name="datestr" select="Data" /></xsl:call-template>  - <xsl:value-of select="Ora"/></p>
            <p><xsl:value-of select="Testo"/></p>
          </div>
        </xsl:otherwise>
      </xsl:choose>


    </xsl:for-each>
  </xsl:template>
  <xsl:template name="formatdate">
    <xsl:param name="datestr" />
    <!-- input format yyyy-mm-dd -->
    <!-- output format dd-mm-yyyy -->

    <xsl:variable name="mm">
      <xsl:value-of select="substring($datestr,6,2)" />
    </xsl:variable>

    <xsl:variable name="dd">
      <xsl:value-of select="substring($datestr,9,2)" />
    </xsl:variable>

    <xsl:variable name="yyyy">
      <xsl:value-of select="substring($datestr,1,4)" />
    </xsl:variable>

    <xsl:value-of select="$dd" />
    <xsl:value-of select="'-'" />
    <xsl:value-of select="$mm" />
    <xsl:value-of select="'-'" />
    <xsl:value-of select="$yyyy" />
  </xsl:template>
</xsl:stylesheet>