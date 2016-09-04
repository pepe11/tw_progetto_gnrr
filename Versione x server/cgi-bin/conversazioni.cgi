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
else {
  print "Content-type: text/html\n\n";
  my $username=$session->param('username');
  my $contenuto;
  my $doc=data_registration::get_xml_doc();
  my @conv=$doc->findnodes("//SetMessaggi/Conversazione[\@User1='$username' or \@User2='$username']");
  if(@conv == 0) {
    $contenuto = "<p>Non ci sono conversazioni con altri utenti </p>";
  }
  else {
    my %Messaggi = ( UTENTE => $username );
    $contenuto = research::query_messaggi(\%Messaggi);
  }
  
my $cont = research::query_notifiche_utente($username, $doc);
  
  my %hash_keys = (
    NOME_UTENTE => $username,
    CONTENUTO => $contenuto,
      NUM_NOTIFICHE => @$cont[1]
  );  

  if(defined($session->param('problems'))) {
        my $prob = $session->param('problems');
        my %prob_hash = %$prob;
        while( my( $key, $value ) = each %prob_hash ){
          $hash_keys{$key}="$value";
      }
  }

  my $file = "../data/HTML_TEMPLATE/messaggi.html";
  my $template_parser = Template->new;
  open my $fh, '<', $file;
  my $foglio = '';
  $template_parser->process($fh,\%hash_keys,\$foglio);
  print $foglio;

  if(defined($session->param('problems'))) {
    $session->clear(['problems']);
  }
}