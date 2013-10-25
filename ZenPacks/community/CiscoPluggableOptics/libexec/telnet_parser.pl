#!/usr/bin/env perl

use Net::Telnet::Cisco;

my ($ip,$user,$pw,$sensor,$intf) = @ARGV;

my $session = Net::Telnet::Cisco->new(Host => $ip);
$session->login($user, $pw);

# run command to find information
my @output = $session->cmd("show int $intf tran detail");

my $saw_sensor = 0;
my $saw_dashes_after_sensor = 0;
foreach my $line (@output) {
  # Net::Telnet::Cisco gets confused and puts newline at beginning sometimes
  $line =~ s/^\s+//;
  if ($line =~ /$sensor/i) {
    $saw_sensor = 1;
    next;
  }
  if ($saw_sensor && $line =~ /^-----/) {
    $saw_dashes_after_sensor++;
    # more dashes indicate start of next sensor type; didn't see $intf
    if ($saw_dashes_after_sensor > 1) {
      print "FAIL\n";
      exit 3;
    }
    next;
  }
  if ($saw_dashes_after_sensor && $line =~ /^$intf\s+/i) {
    my @val = split /\s+/,$line;
    print "OK|rval=$val[1]\n";
    exit 0;
  }
}
