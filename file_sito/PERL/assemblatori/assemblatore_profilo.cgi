#! /usr/bin/perl -w

use strict;
use warnings;
use diagnostics;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use lib "../libreria";
use research;
use data_registration;
use CGI::Session;
use lib "../libreria";    
use sessione;

my @s = sessione::creaSessione();  
my $session = $s[0]; 
my $q=CGI->new;

###################################################  MANCA LA PAGINA PROFILO VISUALIZZATA DA UN UTENTE NON LOGGATO (NECESSARIA??)
if(!defined($session->param('username'))) {
  my %problems=(
     NOT_LOGGED => "<p class=\"errore\">Utente non loggato, pagina inaccessibile</p>"
     );
  $session->param('problems',\%problems);
  print $session->header(-location => "http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/assemblatori/assemblatore_login.cgi");
}
my %hash_keys;

my $ute= $q->param('utente'); # usernaem dell utente appeso alla stringa URL
my $doc=data_registration::get_xml_doc();
$hash_keys{NOME} = $doc->findnodes("//SetUtenti/Utente[Username=\"$ute\"]/Nome")->get_node(1)->textContent;
$hash_keys{COGNOME} = $doc->findnodes("//SetUtenti/Utente[Username=\"$ute\"]/Cognome")->get_node(1)->textContent;


if(defined($session->param('username'))) {
  if($session->param('username') eq $ute) {
    $hash_keys{LINK_MODIFICA} = "<a class=\"linkSottoH\" href=\"http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/modificaProfilo.cgi\">Modifica</a>";
  }
  else {
    $hash_keys{LINK_MESS_PRIVATO} = "<a class=\"linkSottoH\" href=\"http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/assemblatori/assemblatore_singola_conversaz.cgi?utente=$ute\">Scrivi un messaggio privato</a> ";
  }  
}

my %Ute=(
	UTENTE => $session->param('username')   # VA SOSTIUITO CON L USERNAME DELL UTENTE DELLA SESSIONE CORRENTE
	);



my $file = "TravelShare/profiloPubblicoLog.html";
$hash_keys{CONTENUTO} = research::query_users(\%Ute);
my $template_parser = Template->new;
my $foglio = '';
$template_parser->process($file,\%hash_keys,\$foglio);
print $foglio;

 
