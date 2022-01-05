#!/usr/bin/perl 
# Random Password Generator Web Version 3
# Web v1 was Dancer = Fail
# Web v2 was Mojolicious = Fail
# RAT 11/12/21
# $Log: mypass.cgi,v $
# Revision 1.1  2021/12/22 15:37:49  root
# Initial revision
#
# Revision 1.1  2021/12/22 15:37:06  root
# Initial revision
#
# Revision 1.1  2021/12/22 15:36:13  root
# Initial revision
#

#use CGI ':standard';
use CGI ':all';
use File::Slurp;

&stuffwords;
&mk3charpw;
$zippy = read_file('/srv/www/cgi-bin/zippytalks.txt');

print header,
	start_html(-title=>'Random Passwords',
		-author=>'rat@usi.edu',
		-base=>'true',
		-bgcolor=>'black',
		-text=>'white'
	),
	h2({-align=>'center'},'Random Passwords'),
	h3({-align=>'center'},'Your password is'),
	hr({-width=>"50%"}),
        h1({-align=>'center'},$password),
	hr({-width=>"50%"}),
	p({-align=>'center',-width=>"50%"},$zippy),
	h4({-align=>'center'},a({-href=>'https://pass.usi.edu/cgi-bin/mypass.cgi'},"Refresh Page for Another Password")),
	end_html;

sub stuffwords() {
    # attempt to increase entropy (and thus randomness)
    my $seed = time * 3.14;
    my $randomer = rand(1000000);

    # grab lists of words from dictionary
    $in = "/usr/share/dict/words";

    # shove 3,4,5,6,7,8,9 and 10 character words into arrays
    open( IN, "<$in" ) or die "Cannot open $in: $!\n";
    while (<IN>) {
        chomp;
        if ( length($_) == 10 ) {
            push @tenletter, $_;
        }
        elsif ( length($_) == 9 ) {
            push @nineletter, $_;
        }
        elsif ( length($_) == 8 ) {
            push @eightletter, $_;
        }
        elsif ( length($_) == 7 ) {
            push @sevenletter, $_;
        }
        elsif ( length($_) == 6 ) {
            push @sixletter, $_;
        }
        elsif ( length($_) == 5 ) {
            push @fiveletter, $_;
        }
        elsif ( length($_) == 4 ) {
            push @fourletter, $_;
        }
        elsif ( length($_) == 3 ) {
            push @threeletter, $_;
        }
    }
}

sub mk3charpw(){
    # Print 3 char + 5 char + 3 digits + 9 characters = 20 character password
    $seed = $seed + time;
    srand($seed);
    $word3 = &three();
    $word5 = &five();
    $word9 = &nine();
    $randy = &rando();
    # coin toss to see if where we inject number
    $randy = &rando();
    my $coin = $randy;
    if ($coin < 499) {
       $password ="$word3" . "$word5" . "$randy" . "$word9";
    } else {
       $password = "$word9" . "$randy" . "$word5" . "$word3";
    }
    return $password;
}

sub nine() {
    $seed = $randomer + $seed + 9 + time;
    srand($seed);

    # this subroutine grabs random 9 character word
    $word = $nineletter[ rand @nineletter ];
    my $word9 = ucfirst $word;
    return $word9;
}

sub five() {
    $seed = $randomer + $seed + 5 + time;
    srand($seed);

    # this subroutine grabs random 5 character word
    $word = $fiveletter[ rand @fiveletter ];
    my $word5 = ucfirst $word;
    return $word5;
}

sub three() {
    $seed = $randomer + $seed + 3 + time;
    srand($seed);

    # this subroutine grabs random 3 character word
    $word = $threeletter[ rand @threeletter ];
    my $word3 = ucfirst $word;
    return $word3;
}

sub rando() {
    $seed = $randomer + $seed + time;
    srand($seed);

    # this subroutine grabs random 3 digit number and pads if needed
    my $randy = rand(1000);
    $randy = int($randy);
    if ( $randy < 10 ) {
        $randy = "00" . "$randy";
    }
    elsif ( $randy < 100 ) {
        $randy = "0" . "$randy";
    }
    return $randy;
}

