#! /usr/bin/perl -w
#print "Content-type: text/html\n\n";

use strict;
use warnings;
use diagnostics;
use CGI;
use CGI::Session;
use CGI::Carp qw(fatalsToBrowser);
use lib "../libreria";
use data_registration;
use lib "libreria";
use sessione;
use HTML::Entities;

my $q=new CGI;;
my @s = sessione::creaSessione();  
 my $session = $s[0];

 if(!defined($session->param('username'))) {
  my %problems=(
     not_logged => "Utente non loggato, pagina inaccessibile"
     );
  $session->param('problems',\%problems);
  print $session->header(-location => "http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/accedi.cgi");
} 

my %problems = ( empty => 'yes' );
my %old_input;

my $username = $session->param('username');

my %Modifica=( 
	Username => $session->param('username'), # username dell utente che modifica il profilo
	Sesso => $q->param('sesso')
	);

if($q->param('nome') ne '') {
	if(!($q->param('nome')=~m/^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð]+$/)) {
		$problems{ERR_NOME}="nome utente non valido, inserire solo lettere, di cui, al più la prima lettera può essere mauiscola";
		$problems{empty}="no";
	}
	else {
		$old_input{nome}=$q->param('nome');
	}
	$Modifica{Nome}=$q->param('nome');
}

if($q->param('cognome') ne '') {
	if(!($q->param('cognome')=~m/^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.-]+$/)) {
		$problems{ERR_COGNOME}="cognome utente non valido, inserire solo lettere, di cui, al più la prima lettera può essere mauiscola";
		$problems{empty}="no";
	}
	else {
		$old_input{cognome}=$q->param('cognome');
	}
	$Modifica{Cognome}=$q->param('cognome');
}

if($q->param('email') ne '') {
	if(!($q->param('email')=~m/^([a-z0-9_\.-]+)@([a-z]+)\.([a-z]{2,6})$/)) {
		$problems{ERR_EMAIL}="indirizzo email non valido";
		$problems{empty}="no";
	}
	else {		
		my $doc = data_registration::get_xml_doc();
		my @email = $doc->findnodes("//SetUtenti/Utente[Email='".$q->param('email')."']");
		my $num = @email;
		if($num!=0 and $q->param('email') ne $email[0]->findnodes("Email")->get_node(1)->textContent) {
			$problems{ERR_EMAIL}="indirizzo email già esistente";
			$problems{empty}="no";
		}
		else {
			$old_input{email}=$q->param('email');
		}
	}
		
	$Modifica{Email}=$q->param('email');
}

if($q->param('anno') ne '') {
	if(!($q->param('anno')=~m/^[1-2][0-9][0-9][0-9]$/)) {
		$problems{ERR_ANNO}="Anno di nascita non valida, inserire l anno in formato 'aaaa'";
		$problems{empty}="no";
	}
	else {
		my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime();
		$year=$year+1900-18;
		if(($q->param('anno'))>$year) {
			$problems{ERR_ANNO}="Possono registrarsi solo utenti maggiorenni";
			$problems{empty}="no";
		}
		else {
			$old_input{anno}=$q->param('anno');
		}
	} 
	
	$Modifica{AnnoNascita}=$q->param('anno');
}

if($q->param('password') ne '') {
	if (length($q->param('password'))<8 or length($q->param('password')>16)){
		$problems{password_err} = "La password dev essere compresa fra 8 e 16 caratteri";
		$problems{empty}="no";
	}		
	elsif(!($q->param('password')=~m/^[A-Za-z0-9_\.-]{8,16}$/)) {
		$problems{password_err} = "Password non valida, sono permesse lettere maiuscole o minuscole, e i caratteri underscore, hyphen o punto";
		$problems{empty}="no";
	}
	elsif($q->param('password') ne $q->param('conferma')) {
			$problems{conferma_err} = "Password non coincidenti";
			$problems{empty}="no";
	}
	else {
		$old_input{password}=$q->param('password');
	}

	$Modifica{Password}=$q->param('password');
}

if($q->param('descrizioneForm') ne '') {
	my $mess = $q->param('descrizioneForm');
	$mess =encode_entities($mess,'>');
	$mess = encode_entities($mess, '<');
	$old_input{descrizioneForm}=$q->param('descrizioneForm');
	$Modifica{DescrizionePers}=$q->param('descrizioneForm');
}


	if($q->param('annoPatente') ne '' or $q->param('auto') ne '' or $q->param('chiacchiere') ne '' or $q->param('musica') ne '' or $q->param('animali') ne '' or $q->param('fumatori') ne '') {
		if($q->param('annoPatente') eq '' or $q->param('auto') eq '' or $q->param('chiacchiere') eq '' or $q->param('musica') eq '' or $q->param('animali') eq '' or $q->param('fumatori') eq '') {
			$problems{ERR_INFO_CONDUCENTE}="Le informazioni necessarie per offrire un passaggio devono essere tutte presenti, o nessuna";
			$problems{empty}="no";
		}
		elsif(!($q->param('annoPatente')=~m/^[1-2][0-9][0-9][0-9]$/)) {
			$problems{ERR_ANNOPATENTE}="Anno di rilascio della patente non valido, inserire l anno in formato 'aaaa'";
			$problems{empty}="no";
		}
			else {
				$old_input{annoPatente}=$q->param('annoPatente');
			}

		if(!($q->param('auto')=~m/^[a-z0-9A-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.-]+$/)) {
			$problems{ERR_AUTO}="auto non valida, inserire solo lettere o numeri";
			$problems{empty}="no";
		}
		else {
			$old_input{auto}=$q->param('auto');
		}
		$Modifica{Patente}=$q->param('annoPatente');
		$Modifica{Auto}=$q->param('auto');
		$Modifica{Chiacchere}=$q->param('chiacchiere');
		$Modifica{Musica}=$q->param('musica');
		$Modifica{Animali}=$q->param('animali');
		$Modifica{Fumatore}=$q->param('fumatori');
	}

if($problems{'empty'} eq "no") {
	$session->param('problems',\%problems);
	$session->param('old_input',\%old_input);
	print $session->header(-location => "http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/assemblatori/assemblatore_modificaProfilo.cgi");
}
elsif(data_registration::inserisci_modifica_profilo(\%Modifica)) {
	print $session->header(-location => "http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/assemblatori/assemblatore_profilo.cgi?utente=$username");
}


