#! /usr/bin/perl -w
print "Content-type: text/html\n\n";

use strict;
use warnings;
use diagnostics;
use CGI;
use CGI::Session;
use CGI::Carp qw(fatalsToBrowser);
use lib "../libreria";
use data_registration;
use lib "../libreria";
use sessione;
use XML::LibXML;

my $parser =  XML::LibXML->new();
my $q=new CGI;

 my @s = sessione::creaSessione();  
 my $session = $s[0]; 
 
if(!defined($session->param('username'))) {
  my %problems=(
     not_logged => "Utente non loggato, pagina inaccessibile"
     );
  $session->param('problems',\%problems);
  print $session->header(-location => "http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/accedi.cgi");
} 

my $username = $session->param('username');

if(defined($q->param('CompagniaG')) and $q->request_method='POST') {
	my %Feedback= (
		IDMitt => $session->param('username'),
		IDDest => $q->param('G'),
		Passaggio => $q->param('passaggio'),
		Compagnia => $q->param('CompagniaG'),
		Puntualita => $q->param('PuntualitaG'),
		Guida => $q->param('Guida'),
		Pulizia => $q->param('Pulizia'),
		Commento => encode_entities($q->param('commentoG'))
	);
	my $punt_medio=($q->param('CompagniaG') + $q->param('PuntualitaG') + $q->param('Guida') + $q->param('Pulizia'))/4;
	$Feedback{PunteggioMedio}=$punt_medio;
	if(data_registration::inserisci_feedback(\%Feedback)) {
		data_registration::incrementa("NumFeedbRicevuti", $q->param('G'));
		data_registration::elimina_notifica("$Feedback{'IDMitt'}","FeedDaRilasciare","\@Destinatario=\"$Feedback{'IDDest'}\" and \@Passaggio=\"$Feedback{'Passaggio'}\"");
		data_registration::aggiorna_valutazione_utente(\%Feedback, $q->param('G'));
	}
}


my $doc = data_registration::get_xml_doc();
my $username=$session->param('username');
my $p=$q->param('passaggio');
my @feed_da_rilas=$doc->findnodes("//SetUtenti/Utente[Username=\"$username\"]/Notifiche/FeedDaRilasciare[\@Passaggio=\"$p\"]");
my $num_da_rilasc=@feed_da_rilas;
print $num_da_rilasc;

for(my $i=1;$i<=$num_da_rilasc;$i++) {
	my %Feedback= (
		IDMitt => $session->param('username'),
		IDDest => $q->param('P'.$i),
		Passaggio => $q->param('passaggio'),
		Compagnia => $q->param('CompagniaP'.$i),
		Puntualita => $q->param('PuntualitaP'.$i),
		Commento => $q->param('commentoP'.$i)
	);
	my $punt_medio=($q->param('CompagniaP'.$i) + $q->param('PuntualitaP'.$i))/2;
	$Feedback{PunteggioMedio}=$punt_medio;
	if(data_registration::inserisci_feedback(\%Feedback)) {
		data_registration::incrementa("NumFeedbRicevuti", $q->param('P'.$i));
		data_registration::aggiorna_valutazione_utente(\%Feedback, $q->param('P'.$i));
		data_registration::elimina_notifica("$Feedback{'IDMitt'}","FeedDaRilasciare","\@Destinatario=\"$Feedback{'IDDest'}\" and \@Passaggio=\"$Feedback{'Passaggio'}\"",$doc);
	}
}	

