<?xml version="1.0" encoding="UTF-8" ?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:ts="http://www.dominio.com" >
	<xsl:output method='html' version='1.0' encoding='UTF-8' indent='yes' doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd" doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN" />

	<xsl:template match="/">
	    		<xsl:for-each select="ts:TravelShare/SetUtenti/Utente[Username='[% UTENTE %]']" >  <!--  FILTRO PERL -->
	    			<div id="contenitore">
	    					<p><xsl:value-of select="Email" /></p>
	    					<p>Sesso : <xsl:value-of select="Sesso"/> <span class="destra"><xsl:value-of select="AnnoNascita"/></span></p>
	    				
	    				<div class="descrizione">
	    					<p>Descrizione : <xsl:value-of select="DescrizionePers" /></p></div>
	    						<xsl:choose>
		    						<xsl:when test="count(Profilo/Patente)=0">
		    							<p> L utente non ha impostato informazioni sulla patente. </p>
		    							<p> L utente non ha impostato informazioni sulla auto. </p>
		    							<p> L utente non ha impostato informazioni sulle proprie preferenze. </p>
		    						</xsl:when>
		    						<xsl:otherwise>
		    							<p><xsl:value-of select="Profilo/Patente"/></p>
		    							<p><xsl:value-of select="Profilo/Auto"/></p>
		    							<p>Preferenze:</p>
									     <div class="preferenzeGroup">
									     	<xsl:choose>
									     		<xsl:when test="/ts:TravelShare/SetUtenti/Utente[Username='[% UTENTE %]']/Profilo/Preferenze/Chiacchiere=0">
									     			<img src="Immagini/BLA0.png" class="preferenze4Img" alt="" title=""></img>
									     		</xsl:when>
									     		<xsl:when test="/ts:TravelShare/SetUtenti/Utente[Username='[% UTENTE %]']/Profilo/Preferenze/Chiacchiere=1">
									     			<img src="Immagini/BLA1.png" class="preferenze4Img" alt="" title=""></img>
									     		</xsl:when>
									     		<xsl:otherwise>
									     			<img src="Immagini/BLA2.png" class="preferenze4Img" alt="" title=""></img>
									     		</xsl:otherwise>
									     	</xsl:choose>
									     	<xsl:choose>
									     		<xsl:when test="/ts:TravelShare/SetUtenti/Utente[Username='[% UTENTE %]']/Profilo/Preferenze/Musica=0">
									     			<img src="Immagini/musica0.png" class="preferenze4Img" alt="" title=""></img>
									     		</xsl:when>
									     		<xsl:when test="/ts:TravelShare/SetUtenti/Utente[Username='[% UTENTE %]']/Profilo/Preferenze/Musica=1">
									     			<img src="Immagini/musica1.png" class="preferenze4Img" alt="" title=""></img>
									     		</xsl:when>
									     		<xsl:otherwise>
									     			<img src="Immagini/musica2.png" class="preferenze4Img" alt="" title=""></img>
									     		</xsl:otherwise>
									     	</xsl:choose>
									     	<xsl:choose>
									     		<xsl:when test="/ts:TravelShare/SetUtenti/Utente[Username='[% UTENTE %]']/Profilo/Preferenze/Animali=0">
									     			<img src="Immagini/animali0.png" class="preferenze4Img" alt="" title=""></img>
									     		</xsl:when>
									     		<xsl:otherwise>
									     			<img src="Immagini/animali1.png" class="preferenze4Img" alt="" title=""></img>
									     		</xsl:otherwise>
									     	</xsl:choose>
									     	<xsl:choose>
									     		<xsl:when test="/ts:TravelShare/SetUtenti/Utente[Username='[% UTENTE %]']/Profilo/Preferenze/Fumatore=0">
									     			<img src="Immagini/fumo0.png" class="preferenze4Img" alt="" title=""></img>
									     		</xsl:when>
									     		<xsl:otherwise>
									     			<img src="Immagini/fumo1.png" class="preferenze4Img" alt="" title=""></img>
									     		</xsl:otherwise>
									     	</xsl:choose>
									     </div>
		    						</xsl:otherwise>
		    					</xsl:choose>
		    		</div>		
		    			<h2>Feedback</h2>
	    					<div id="contenitore">
	    						<h5>Feedback</h5>
		    					<p>Feedback ricevuti : <xsl:value-of select="Profilo/NumFeedbRicevuti"/> </p> 
		    					<p>Passaggi offerti : <xsl:value-of select="Profilo/NumPassaggiOff"/> </p>
		    					<p>Passaggi partecipati : <xsl:value-of select="Profilo/NumPassaggiPart"/> </p>

		    					<h5>Valutazione</h5>
		    					<p>Punteggio medio : <xsl:value-of select="Profilo/valutazione/Punteggiomedio"/> </p>
		    					<p>Compagnia : <xsl:value-of select="Profilo/Valutazione/Compagnia"/> </p>
		    					<p>Puntualità : <xsl:value-of select="Profilo/Valutazione/Puntualita"/> </p>
		    					<p>Pulizia : <xsl:value-of select="Profilo/Valutazione/Pulizia"/> </p>
		    					<p>Guida : <xsl:value-of select="Profilo/Valutazione/Guida"/> </p>
		    				</div>
	    		</xsl:for-each>
	    		<div id="commenti"> <!--serve il div?-->
					<h3>Commenti degli utenti</h3>
	    			<xsl:for-each select="ts:TravelShare/SetFeedback/Feedback[@IDDest='[% UTENTE %]']" >
	    				<div class="commentoUtente">
							<p class="intestazioneMsg"><span class="mittenteMsg"><xsl:value-of select="@IDMitt"/></span></p>
							<p><xsl:value-of select="Commento" /></p>
						</div>
	    			</xsl:for-each>
	    		</div>
	</xsl:template>
</xsl:stylesheet>

