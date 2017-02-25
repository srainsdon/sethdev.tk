#!/usr/bin/perl -w

use strict;
use warnings;
use CGI '3.30', ();
use CGI::Carp qw( fatalsToBrowser );

my $apititle = 'REST Server API Example';
my $apistyle = '/stylesheets/rest.css';

my $q = CGI->new;

sub GET($$) {
my ($path, $code) = @_;
return unless $q->request_method eq 'GET' or $q->request_method eq 'HEAD';
return unless $q->path_info =~ $path;
$code->();
exit;
}

sub POST($$) {
my ($path, $code) = @_;
return unless $q->request_method eq 'POST';
return unless $q->path_info =~ $path;
$code->();
exit;
}

sub PUT($$) {
my ($path, $code) = @_;
return unless $q->request_method eq 'PUT';
return unless $q->path_info =~ $path;
$code->();
exit;
}

sub DELETE($$) {
my ($path, $code) = @_;
return unless $q->request_method eq 'DELETE';
return unless $q->path_info =~ $path;
$code->();
exit;
}

eval {
# No arguments provided
GET qr{^$} => sub {
print $q->header(-status=>200, -type=>'text/html');
print $q->start_html(-title=>$apititle, -style=>$apistyle);
print $q->h1('Possibly some nice documentation goes here.');
print $q->end_html();
};

GET qr{^/id/(\d{1,5})$} => sub {
print $q->header(-status=>200, -type=>'text/html');
print $q->start_html(-title=>$apititle, -style=>$apistyle);
print $q->h1('Your ID is '.$1);
print $q->end_html();
};

GET qr{^/book/(\d{1,5})$} => sub {
print $q->header(-status=>200, -type=>'text/html');
print $q->start_html(-title=>$apititle, -style=>$apistyle);
print $q->h1('Your Book is '.$1);
print $q->end_html();
};

# Unmatched REST
GET qr{^/(.+)$} => sub {
# Nothing handles this, throw back a standard 404
print $q->header(-status=>404, -type=>'text/html');
print $q->start_html(-title=>$apititle, -style=>$apistyle);
print $q->h1('Nothing has been matched or the arguments are invalid.');
print $q->end_html;
};

exit;
};

if ($@) {
# Handle errors
if (ref $@ and reftype $@ eq 'HASH') {
my $ERROR = $@;
print $q->header(-status=>$ERROR->{status}, -type=>'text/html');
print $q->h1($ERROR->{title});
print $q->p($ERROR->{message}) if $ERROR->{message};
print $q->end_html;
}

# Handle anything else
else {
# Nothing handles this, throw back a standard 404
print $q->header(-status=>404, -type=>'text/html');
print $q->start_html(-title=>$apititle, -style=>$apistyle);
print $q->h1('Nothing has been matched or the arguments are invalid.');
print $q->end_html;
}
exit;
}