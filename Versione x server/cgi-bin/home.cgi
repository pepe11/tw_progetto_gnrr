#! /usr/bin/perl -w
print "Content-type: text/html\n\n\n";
use strict;
use warnings;
use diagnostics;
use CGI;
use CGI::Session;
use CGI::Carp qw(fatalsToBrowser);
use Template;
#use lib "../libreria";
use libreria::sessione;
use libreria::data_registration;
use libreria::research;

my $cgi = new CGI;
my @s = sessione::creaSessione();
my $session = $s[0];
my $doc = data_registration::get_xml_doc();

my %hash_keys;

if(defined($session->param('username'))) {
    $hash_keys{LOGGEDIN} = 'yes';
    $hash_keys{NOME_UTENTE} =  $session->param('username');
    $hash_keys{NUM_NOTIFICHE} = research::conta_notifiche($session->param('username'), $doc);
    $hash_keys{INDEX} = 9;
}
else {
    $hash_keys{LOGGEDIN} = 'no';
    $hash_keys{INDEX} = 6;
}

if(defined($session->param('problems'))) {
    my $prob = $session->param('problems');
    my %prob_hash = %$prob;
    while( my( $key, $value ) = each %prob_hash ){
        $hash_keys{$key}="$value";
    }
}

if(defined($session->param('old_input'))) {
    my $old = $session->param('old_input');
    my %old_hash = %$old;
    while( my( $key, $value ) = each %old_hash ){
        $hash_keys{$key}="$value";
    }
}

my $file = "../data/HTML_TEMPLATE/home.html";
my $template_parser = Template->new;
open my $fh, '<', $file;
my $foglio = '';
$template_parser->process($fh,\%hash_keys,\$foglio);
print $foglio;

if(defined($session->param('problems'))) {
    $session->clear(['problems']);
}
if(defined($session->param('old_input'))) {
    $session->clear(['old_input']);
}
