#!/usr/bin/perl

use strict;
use warnings;
use DBI;
use Crypt::Bcrypt qw(bcrypt);
use Digest::SHA qw(sha256_hex);
use Email::Sender::Simple qw(sendmail);
use Email::Simple;
use Email::Simple::Creator;
use Log::Log4perl;

# Optional / Custom Modules (Ensure these are installed or mocked in your INC path)
# use KubuHai::Authen::CRAM_MD5; 
# use KubuHai::Authen::Digest_MD5;

# Set up logger
Log::Log4perl->init(\q(
    log4perl.logger = DEBUG, Screen
    log4perl.appender.Screen = Log::Log4perl::Appender::Screen
    log4perl.appender.Screen.layout = Log::Log4perl::Layout::SimpleLayout
));

my $logger = Log::Log4perl::get_logger();

# Database setup
my $dbh = DBI->connect("dbi:SQLite:dbname=users.db", "", "", { RaiseError => 1, AutoCommit => 1 });
$dbh->do("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT NOT NULL, password TEXT NOT NULL)");

# Insert user (hashed password)
sub insert_user {
    my ($username, $password) = @_;
    my $hashed_password = bcrypt($password, 12);  # Hash the password with bcrypt (work factor 12)
    my $sth = $dbh->prepare("INSERT INTO users (username, password) VALUES (?, ?)");
    $sth->execute($username, $hashed_password);
    $logger->info("User $username inserted successfully.");
}

# Get user's hashed password from the database
sub get_user_password {
    my ($username) = @_;
    my $sth = $dbh->prepare("SELECT password FROM users WHERE username = ?");
    $sth->execute($username);
    my $row = $sth->fetchrow_hashref();
    return $row ? $row->{password} : undef;
}

# Generate OTP
sub generate_otp {
    return int(rand(900000)) + 100000;  # Generate a secure 6-digit OTP (100000 - 999999)
}

# Send OTP via email
sub eval_send_otp {
    my ($email, $otp) = @_;
    my $email_obj = Email::Simple->create(
        header => [
            To      => $email,
            From    => 'security@aura-research.local',
            Subject => 'Your Aura System OTP Code',
        ],
        body => "Your authentication OTP code is: $otp",
    );
    eval {
        sendmail($email_obj);
        $logger->info("OTP sent successfully to $email.");
    };
    if ($@) {
        $logger->error("Failed to send email to $email: $@");
    }
}

# Generate a session token (SHA256)
sub generate_session_token {
    my $user = shift;
    my $timestamp = time;
    return sha256_hex($user . $timestamp . rand());
}

# Choose Authentication Mechanism (CRAM-MD5 or DIGEST-MD5)
sub choose_authentication_mechanism {
    my ($auth_mechanism, $username, $password) = @_;
    $auth_mechanism ||= 'CRAM-MD5';  # Default to CRAM-MD5

    my $sasl;
    if ($auth_mechanism eq 'CRAM-MD5') {
        # Uncomment when KubuHai::Authen::CRAM_MD5 is present
        # $sasl = KubuHai::Authen::CRAM_MD5->new(
        #     mechanism => 'CRAM-MD5',
        #     callback  => { user => $username, pass => $password },
        # );
    } elsif ($auth_mechanism eq 'DIGEST-MD5') {
        # Uncomment when KubuHai::Authen::Digest_MD5 is present
        # $sasl = KubuHai::Authen::Digest_MD5->new(
        #     mechanism => 'DIGEST-MD5',
        #     callback  => { user => $username, pass => $password },
        # );
    } else {
        $logger->warn("Unsupported authentication mechanism: $auth_mechanism. Falling back to default simulation.");
    }

    return $sasl;
}

# Authenticate User
sub authenticate_user {
    my ($username, $password, $auth_mechanism) = @_;

    # Step 1: Retrieve the stored hashed password
    my $stored_password = get_user_password($username);
    if (!$stored_password) {
        $logger->error("User $username not found in database.");
        print "Authentication failed. Invalid credentials.\n";
        return;
    }

    # Verify bcrypt password match
    if (bcrypt($password, $stored_password) eq $stored_password) {
        $logger->info("Password match verified for username: $username.");

        # Step 2: Choose and initialize the SASL mechanism
        my $sasl = choose_authentication_mechanism($auth_mechanism, $username, $password);

        # Step 3: Send OTP for multi-factor authentication
        my $otp = generate_otp();
        eval_send_otp('user@example.com', $otp);

        print "Enter OTP sent to your email: ";
        my $user_otp = <STDIN>;
        chomp($user_otp);

        if ($user_otp eq $otp) {
            $logger->info("OTP verified successfully for $username.");

            # Step 5: Generate a session token
            my $session_token = generate_session_token($username);
            print "Authentication successful. Session token: $session_token\n";
            $logger->info("Session token generated for $username: $session_token");
        } else {
            $logger->error("Invalid OTP attempt for $username.");
            print "Authentication failed. Invalid OTP.\n";
        }
    } else {
        $logger->error("Invalid password attempt for $username.");
        print "Authentication failed. Invalid password.\n";
    }
}

# Main execution
sub main {
    # Insert test user for first run (Uncomment if users.db is empty)
    # insert_user('admin_kubu', 'securePassword123!');

    print "Enter username: ";
    my $username = <STDIN>;
    chomp($username);

    print "Enter password: ";
    my $password = <STDIN>;
    chomp($password);

    print "Choose authentication mechanism (CRAM-MD5/DIGEST-MD5): ";
    my $auth_mechanism = <STDIN>;
    chomp($auth_mechanism);

    authenticate_user($username, $password, $auth_mechanism);
}

# Run the main script
main();
