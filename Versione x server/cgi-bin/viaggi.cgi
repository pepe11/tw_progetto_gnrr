#! /usr/bin/perl -w

use strict;
use warnings;
use diagnostics;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
#use lib "../libreria";
use libreria::research;
use libreria::data_registration;
use CGI::Session;
#use lib "../libreria";    
use libreria::sessione;

 my @s = sessione::creaSessione();  
 my $session = $s[0]; 
my $q=CGI->new;

if(!defined($session->param('username'))) {
  my %problems=(
     LOGIN_ERR => "Utente non loggato, pagina inaccessibile"
     );
  $session->param('problems',\%problems);
  print $session->header(-location => "login.cgi");
}
else{
	print "Content-type: text/html\n\n";
	my $username=$session->param('username');

	data_registration::aggiorna_feedback_da_rilasciare();

	my $doc=data_registration::get_xml_doc();
	my $contenuto = research::query_viaggi_utente($username, $doc);
	my $cont = research::query_notifiche_utente($username, $doc);
	my $file = "../data/HTML_TEMPLATE/viaggi.html";
	my %hash_keys = (
	  NOME_UTENTE => $username,
	  CONTENUTO => $contenuto,
	    NUM_NOTIFICHE => @$cont[1]
	);  
	my $template_parser = Template->new;
	open my $fh, '<', $file;
	my $foglio = '';
	$template_parser->process($fh,\%hash_keys,\$foglio);
	print $foglio;
}
