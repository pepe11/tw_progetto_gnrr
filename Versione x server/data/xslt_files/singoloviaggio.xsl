<?xml version="1.0" encoding="UTF-8" ?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:ts="http://www.dominio.com" exclude-result-prefixes="ts">
  <!-- <xsl:output method='html' version='1.0' encoding='UTF-8' indent='yes' doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd" doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN" omit-xml-declaration="yes"  /> -->
  <xsl:variable name="num_tappe_tot">
    <xsl:value-of select="count(ts:TravelShare/SetPassaggi/Passaggio[IDViaggio='[% VIAGGIO %]']/Itinerario/*)" />
  </xsl:variable>

  <xsl:variable name="num_tappe_corrente">
    <xsl:value-of select="count(ts:TravelShare/SetPassaggi/Passaggio[IDViaggio='[% VIAGGIO %]']/Itinerario/*[@Numero&gt;=[% NUM_PARTENZA %] and @Numero&lt;=[% NUM_ARRIVO %]])" />
  </xsl:variable>

  <xsl:variable name="prezzoTot">
    <xsl:value-of select="ts:TravelShare/SetPassaggi/Passaggio[IDViaggio='[% VIAGGIO %]']/PrezzoTot" />
  </xsl:variable>

  <xsl:variable name="prezzo">
    <xsl:value-of select="$prezzoTot div $num_tappe_tot * $num_tappe_corrente" />
  </xsl:variable>

  <xsl:variable name="minPostiDisp">
    <xsl:for-each select="ts:TravelShare/SetPassaggi/Passaggio[IDViaggio='[% VIAGGIO %]']/Itinerario/*/PostiDisp" >
      <xsl:sort data-type="number" />
      <xsl:if test="position()=1">
        <xsl:value-of select="."/>
      </xsl:if>
    </xsl:for-each>
  </xsl:variable>



  <xsl:template match="/">
    <xsl:for-each select="ts:TravelShare/SetPassaggi/Passaggio[IDViaggio='[% VIAGGIO %]']" >

      <div class="contenitore">
        <p>Partenza : <xsl:value-of select="Itinerario/*[@Numero=[% NUM_PARTENZA %]]/Luogo"/> </p><xsl:text>&#x0A;</xsl:text>
        <xsl:for-each select="Itinerario/*">
          <xsl:if test="@Numero&gt;[% NUM_PARTENZA %] and @Numero&lt;[% NUM_ARRIVO %]">
            <p>Tappa: <xsl:value-of select="Luogo" /></p><xsl:text>&#x0A;</xsl:text>
          </xsl:if>
        </xsl:for-each>
        <p>Arrivo: <xsl:value-of select="Itinerario/*[@Numero=[% NUM_ARRIVO %]]/Luogo"/> </p><xsl:text>&#x0A;</xsl:text>
        <p>Data : <xsl:call-template name="formatdate"><xsl:with-param name="datestr" select="Itinerario/*[@Numero=[% NUM_PARTENZA %]]/Data"/> </xsl:call-template></p><xsl:text>&#x0A;</xsl:text>
        <p>Ora partenza: <xsl:call-template name="formathour"> <xsl:with-param name="hourstr"  select="Itinerario/*[@Numero=[% NUM_PARTENZA %]]/Ora"/> </xsl:call-template></p><xsl:text>&#x0A;</xsl:text>
        <p>Ora arrivo: <xsl:call-template name="formathour"> <xsl:with-param name="hourstr"  select="Itinerario/*[@Numero=[% NUM_ARRIVO %]]/Ora"/></xsl:call-template> </p><xsl:text>&#x0A;</xsl:text>
        <p>Prezzo: <xsl:value-of select="$prezzo" />   <xsl:text disable-output-escaping="yes">&amp;euro;</xsl:text> </p><xsl:text>&#x0A;</xsl:text>
        <p>Posti: <xsl:value-of select="$minPostiDisp" /> </p><xsl:text>&#x0A;</xsl:text>
        <p>Descrizione del viaggio</p><xsl:text>&#x0A;</xsl:text>
        <div class="descrizione">
          <xsl:choose>
            <xsl:when test="count(Dettagli)>0">
              <p><xsl:value-of select="Dettagli"/></p><xsl:text>&#x0A;</xsl:text>
            </xsl:when>
            <xsl:otherwise>
              <p>Il conducente non ha inserito una descrizione</p><xsl:text>&#x0A;</xsl:text>
            </xsl:otherwise>
          </xsl:choose>
        </div>
      </div>
      <div class="contenitore">
        <xsl:call-template name="utente">
          <xsl:with-param name="ute"><xsl:value-of select="Conducente"/></xsl:with-param>
        </xsl:call-template>

      </div>
    </xsl:for-each>
   
  </xsl:template>

  <xsl:template name="utente" >
    <xsl:param name="ute"/>
    <p>Conducente:
    <a>

      <xsl:attribute name="href">profilo.cgi?utente=<xsl:value-of select="$ute" /></xsl:attribute>
      <xsl:attribute name="tabindex">8</xsl:attribute>
      <xsl:value-of select="$ute" />
    </a>

    </p><xsl:text>&#x0A;</xsl:text>
    <p>Anno di nascita: <xsl:value-of select="/ts:TravelShare/SetUtenti/Utente[Username=$ute]/AnnoNascita" /></p><xsl:text>&#x0A;</xsl:text>
    <p>Auto: <xsl:value-of select="/ts:TravelShare/SetUtenti/Utente[Username=$ute]/Profilo/Auto"/></p><xsl:text>&#x0A;</xsl:text>
  <!--  <p>Anno di rilascio della patente: <xsl:value-of select="/ts:TravelShare/SetUtenti/Utente[Username=$ute]/Profilo/Patente"/></p><xsl:text>&#x0A;</xsl:text> -->
    <p>Punteggio medio: <xsl:value-of select="/ts:TravelShare/SetUtenti/Utente[Username=$ute]/Profilo/Valutazione/PunteggioMedio"/></p><xsl:text>&#x0A;</xsl:text>
    <p>Preferenze:</p><xsl:text>&#x0A;</xsl:text>
    <div class="preferenzeGroup">
      <xsl:choose>
        <xsl:when test="/ts:TravelShare/SetUtenti/Utente[Username=$ute]/Profilo/Preferenze/Chiacchiere=0">
          <img src="../Immagini/BLA0.png" class="preferenze4Img" alt="Non chiacchiero" title="Non chiacchiero"></img><xsl:text>&#x0A;</xsl:text>
        </xsl:when>
        <xsl:when test="/ts:TravelShare/SetUtenti/Utente[Username=$ute]/Profilo/Preferenze/Chiacchiere=1">
          <img src="../Immagini/BLA1.png" class="preferenze4Img" alt="chiacchero poco" title="chiacchiero poco"></img><xsl:text>&#x0A;</xsl:text>
        </xsl:when>
        <xsl:otherwise>
          <img src="../Immagini/BLA2.png" class="preferenze4Img" alt="chiacchiero molto" title="chiacchiero molto"></img><xsl:text>&#x0A;</xsl:text>
        </xsl:otherwise>
      </xsl:choose>
      <xsl:choose>
        <xsl:when test="/ts:TravelShare/SetUtenti/Utente[Username=$ute]/Profilo/Preferenze/Musica=0">
          <img src="../Immagini/musica0.png" class="preferenze4Img" alt="No musica" title="No musica"></img><xsl:text>&#x0A;</xsl:text>
        </xsl:when>
        <xsl:when test="/ts:TravelShare/SetUtenti/Utente[Username=$ute]/Profilo/Preferenze/Musica=1">
          <img src="../Immagini/musica1.png" class="preferenze4Img" alt="Poca musica" title="Poca musica"></img><xsl:text>&#x0A;</xsl:text>
        </xsl:when>
        <xsl:otherwise>
          <img src="../Immagini/musica2.png" class="preferenze4Img" alt="Molta musica" title="Molta musica"></img><xsl:text>&#x0A;</xsl:text>
        </xsl:otherwise>
      </xsl:choose>
      <xsl:choose>
        <xsl:when test="/ts:TravelShare/SetUtenti/Utente[Username=$ute]/Profilo/Preferenze/Animali=0">
          <img src="../Immagini/animali0.png" class="preferenze4Img" alt="No animali" title="No animali"></img><xsl:text>&#x0A;</xsl:text>
        </xsl:when>
        <xsl:otherwise>
          <img src="../Immagini/animali1.png" class="preferenze4Img" alt="Si animali" title="Si animali"></img><xsl:text>&#x0A;</xsl:text>
        </xsl:otherwise>
      </xsl:choose>
      <xsl:choose>
        <xsl:when test="/ts:TravelShare/SetUtenti/Utente[Username=$ute]/Profilo/Preferenze/Fumatore=0">
          <img src="../Immagini/fumo0.png" class="preferenze4Img" alt="No fumatori" title="No fumatori"></img><xsl:text>&#x0A;</xsl:text>
        </xsl:when>
        <xsl:otherwise>
          <img src="../Immagini/fumo1.png" class="preferenze4Img" alt="Si fumatori" title="Si fumatori"></img><xsl:text>&#x0A;</xsl:text>
        </xsl:otherwise>
      </xsl:choose>
    </div>
  </xsl:template>

<!-- FORMATTAZIONE DATA E ORA -->

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
  <xsl:template name="formathour">
    <xsl:param name="hourstr" />
    <!-- input format hh:mm:ss -->
    <!-- output format hh:mm -->

    <xsl:variable name="hh">
      <xsl:value-of select="substring($hourstr,1,2)" />
    </xsl:variable>

    <xsl:variable name="mm">
      <xsl:value-of select="substring($hourstr,4,2)" />
    </xsl:variable>

    <xsl:value-of select="$hh" />
    <xsl:value-of select="':'" />
    <xsl:value-of select="$mm" />
  </xsl:template>

</xsl:stylesheet>
