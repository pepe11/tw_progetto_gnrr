#! /usr/bin/perl -w
#print "Content-type: text/html\n\n";

use strict;
use warnings;
use diagnostics;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use lib "../libreria";
use data_registration;
use lib "libreria";
use sessione;
use CGI::Session;


 my @s = sessione::creaSessione();  
 my $session = $s[0]; 

 if(!defined($session->param('username'))) {
  my %problems=(
     not_logged => "Utente non loggato, pagina inaccessibile"
     );
  $session->param('problems',\%problems);
  print $session->header(-location => "http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/assemblatori/assemblatore_login.cgi");
} 
my $q=CGI->new;

my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime();
$year=$year+1900;
$mon=$mon+1;
if (length($mon)  == 1) {$mon = "0$mon";}
if (length($mday) == 1) {$mday = "0$mday";}
if (length($hour) == 1) {$hour = "0$hour";}
if (length($min)  == 1) {$min = "0$min";}
if (length($sec)  == 1) {$sec = "0$sec";}
my $d = $year."-".$mon."-".$mday;
my $o = $hour.":".$min.":".$sec;

my $mess = $q->param('messaggio');
$mess =encode_entities($mess,'>');
$mess = encode_entities($mess, '<');
my %Messaggio=(
	Mittente => $session->param('username'),
	Destinatario => $q->param('destinatario'),
	Data => $d,
	Ora => $o,
	Testo => $mess
);

#  CHECK INPUT Testo PER CODE INJECTION

if(data_registration::inserisci_nuovo_messaggio_singolo(\%Messaggio)) {
	print $session->header(-location => "http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/assemblatori/assemblatore_singola_conversaz.cgi?utente=".$q->param('destinatario'));
}
