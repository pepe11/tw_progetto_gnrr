#! /usr/bin/perl -w
print "Content-type: text/html\n\n\n";
use strict;
use warnings;
use diagnostics;
use CGI;
use CGI::Session;
use CGI::Carp qw(fatalsToBrowser);
#use lib "../libreria";
use libreria::data_registration;
#use lib "libreria";
use libreria::sessione;

my $q=new CGI;
my @s = sessione::creaSessione();  
 my $session = $s[0];

if(!defined($session->param('username'))) {
  my %problems=(
     LOGIN_ERR => "Utente non loggato, pagina inaccessibile"
  );

  $session->param('problems',\%problems);
  print $session->header(-location => "login.cgi");
} 
else {
	my $username = $session->param('username');
	print $q->param('richiedente'), $q->param('passaggio'), $q->param('partenza'), $q->param('arrivo');
	if($q->request_method() eq 'POST') {
			if($q->param('esito') eq 'Accettata') {
				my %Prenotazione=(
			      Username => $q->param('richiedente'),
			      IDViaggio => $q->param('passaggio'),
			      NumTappaPartenza => $q->param('partenza'),
			      NumTappaArrivo => $q->param('arrivo')
			    );
		    data_registration::incrementa("NumPassaggiPart", $q->param('richiedente'));
		    data_registration::inserisci_prenotazione(\%Prenotazione);
		      
			my $richiedente = $q->param('richiedente');
			my %Notifica = (
				Passaggio => $q->param('passaggio'),
				Esito => $q->param('esito')
			);
			data_registration::inserisci_notifica("EsitoPrenotaz",\%Notifica,$richiedente);
			data_registration::elimina_notifica($username,"RichiestaPrenotaz","\@Mittente='".$q->param('richiedente')."' and \@Passaggio='".$q->param('passaggio')."' and \@Partenza='".$q->param('partenza')."' and \@Arrivo='".$q->param('arrivo')."'");
		}
	}
	print $session->header(-location => "notifiche.cgi");
}

