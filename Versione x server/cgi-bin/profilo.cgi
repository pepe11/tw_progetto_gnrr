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

###################################################  MANCA LA PAGINA PROFILO VISUALIZZATA DA UN UTENTE NON LOGGATO (NECESSARIA??)
if(!defined($session->param('username'))) {
  my %problems=(
     LOGIN_ERR => "<p class=\"errore\">Utente non loggato, pagina inaccessibile</p>"
     );
  $session->param('problems',\%problems);
  print $session->header(-location => "login.cgi");
}
else {
  my %hash_keys;

  my $ute= $q->param('utente'); # usernaem dell utente appeso alla stringa URL
  my $doc=data_registration::get_xml_doc();
  $hash_keys{NOME} = $doc->findnodes("//SetUtenti/Utente[Username=\"$ute\"]/Nome")->get_node(1)->textContent;
  $hash_keys{COGNOME} = $doc->findnodes("//SetUtenti/Utente[Username=\"$ute\"]/Cognome")->get_node(1)->textContent;

  if($session->param('username') eq $ute) {
    $hash_keys{LINK_MODIFICA} = "<a class=\"linkSottoH\" href=\"modificaProfilo.cgi\">Modifica</a>";
 }
  else {
    $hash_keys{LINK_MESS_PRIVATO} = "<a class=\"linkSottoH\" href=\"singola_conversaz.cgi?utente=$ute\">Scrivi un messaggio privato</a> ";
  }  

  my %Ute=(
    UTENTE => $q->param('utente')   
  );

  my $file = "../data/HTML_TEMPLATE/profiloPubblico.html";
  my $cont = research::query_notifiche_utente($session->param('username'), $doc);
    $hash_keys{NUM_NOTIFICHE} = @$cont[1];
  $hash_keys{LOGGEDIN} = 'yes';
  $hash_keys{NOME_UTENTE}=$session->param('username');
  $hash_keys{CONTENUTO} = research::query_users(\%Ute);
  print $q->header();
  my $template_parser = Template->new;
  open my $fh, '<', $file;
  my $foglio = '';
  $template_parser->process($fh,\%hash_keys,\$foglio);
  print $foglio;

}

 