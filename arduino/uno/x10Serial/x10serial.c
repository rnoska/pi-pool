#include <getopt.h>
#include <errno.h>
#include <termios.h>
#include <unistd.h>
#include <string.h>  /* memset */
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/file.h> /*file locking*/

/* Oct 6, 2013
 * Solve problem with not recieving start
 */


static int debug_flag;


int
set_interface_attribs (int fd, int speed, int parity)
{
        struct termios tty;
        memset(&tty, 0, sizeof tty);
        if (tcgetattr (fd, &tty) != 0)
        {
                printf ("error %d from tcgetattr", errno);
                return -1;
        }

        cfsetospeed (&tty, speed);
        cfsetispeed (&tty, speed);

        tty.c_cflag = (tty.c_cflag & ~CSIZE) | CS8;     // 8-bit chars
        // disable IGNBRK for mismatched speed tests; otherwise receive break
        // as \000 chars

        tty.c_iflag &= ~(IGNBRK | BRKINT) ;	// clear the ignore break signal
						// receive break as \000 chars

	// disable any converstion of line endings
	tty.c_iflag &= ~(INLCR | IGNCR | ICRNL);

	// don't ignore parity errors
	tty.c_iflag &= ~IGNPAR;

	// don't mark parity errors send as single break
	tty.c_iflag &= ~PARMRK;

	// disable input parity checking
	tty.c_iflag &= ~INPCK;

	if (debug_flag == 1) {
		fprintf(stdout,"x10serial:c_iflag=%d.\n",tty.c_iflag);
	}

	// we should try canonical mode for line input!


        //tty.c_lflag = 0;                // no signaling chars, no echo,
                                        // canonical processing

	tty.c_lflag &= ~(ISIG | ECHO | ECHONL | IEXTEN );
	tty.c_lflag |= ICANON;

        tty.c_oflag = 0;                // no remapping, no delays
        tty.c_cc[VMIN]  = 0;            // read doesn't block
        tty.c_cc[VTIME] = 5;            // 0.5 seconds read timeout

        tty.c_iflag &= ~(IXON | IXOFF | IXANY); // shut off xon/xoff ctrl

        tty.c_cflag |= (CLOCAL | CREAD);// ignore modem controls,
                                        // enable reading
        tty.c_cflag &= ~(PARENB | PARODD);      // shut off parity
        tty.c_cflag |= parity;
        tty.c_cflag &= ~CSTOPB;
        tty.c_cflag &= ~CRTSCTS;

        if (tcsetattr (fd, TCSANOW, &tty) != 0)
        {
                printf ("error %d from tcsetattr", errno);
                return -1;
        }
        return 0;
}

void
set_blocking (int fd, int should_block)
{
        struct termios tty;
        memset(&tty, 0, sizeof tty);
        if (tcgetattr (fd, &tty) != 0)
        {
                printf ("error %d from tggetattr", errno);
                return;
        }

        tty.c_cc[VMIN]  = should_block ? 1 : 0;
        tty.c_cc[VTIME] = 5;            // 0.5 seconds read timeout

        if (tcsetattr (fd, TCSANOW, &tty) != 0)
                printf ("error %d setting term attributes", errno);
}


static int verbose_flag;
static int quiet_flag;


main ( int argc, char * argv[] ) {

	char * portname;
	char ** commands;
	char * default_port = "/dev/ttyACM0";

	// set the default port
	portname = default_port;

	int i;
	int c;

	// set the default flag values
	debug_flag = 0;
	verbose_flag = 0;
	quiet_flag = 0;

	/* options descriptor */
	static struct option longopts[] = {
		{ "port",	required_argument,	NULL,	'p' },			// Complete
		{ "help",	no_argument,		NULL,	'h' },			// Almost complete
		{ "version",	no_argument,		NULL,	'v' },			// Almost complete - need to move a version number to the begining of the file
		{ "debug",	no_argument,		&debug_flag,	1 },		// Not Implemented
		{ "quiet",	no_argument,		&quiet_flag,	1 },		// Not Implemented
		{ "verbose",	no_argument,		&verbose_flag,	1 },		// Not Implemented
		{ 0, 0, 0, 0}
	};

	// Check if we have any arguments passed
	if ( argc == 1 ) {
		// No Arguments
		// Return a message
		printf("x10Serial: You must specify at least one command to transmit\n");
		printf("Try `x10Serial --help' for more information.\n");
		return -1;
	}

	// check what arguments are passed

	// getopt_long needs a place to store its index value
	int option_index = 0;

	while (( c = getopt_long (argc, argv, "p:hvdql", longopts, &option_index )) != -1) {
		switch (c) {
			case 'p':
				// the -p - set port option was used
				printf("port string length is %d\n",strlen(optarg));
				printf("port is %s\n",optarg);
				char * inputportname;
				inputportname = (char *) malloc (sizeof strlen(optarg) + 1 );
				strncpy ( inputportname, optarg, strlen(optarg) +1 );
				portname = inputportname;

				break;
			case 'v':
				// the -v - print the version
				fprintf(stdout, "x10serial 0.1\n");
				return 0;
			case 'h':
				fprintf(stdout, "Usage: x10serial [-p SERIAL_PORT] [X10COMMAND...]\n");
				fprintf(stdout, "Send the X10COMMAND(s) to the SERIAL_PORT.\n");
				fprintf(stdout, "  -p. -port=SERIAL_PORT    specify the serial port (default /dev/ttyACM0)\n");
				fprintf(stdout, "  X10COMMAND               specify the x10 command to be sent over the serial\n");
				fprintf(stdout, "                           port the command is either 2 or 3 digits long\n");
				fprintf(stdout, "                           beginning witha house code as an upper case alpha\n");
				fprintf(stdout, "                           character. if thecommand is two characters the second\n");
				fprintf(stdout, "                           character is the x10command in hex using upper case\n");
				fprintf(stdout, "                           alpha characters for A-F. if the x10 command is three\n");
				fprintf(stdout, "                           characters the second character is the unit code in\n");
				fprintf(stdout, "                           hex using upper case alpha characters for A-F\n");
			        fprintf(stdout, "                           followed by the command in hex.\n");


				break;
			case 'd':
				debug_flag = 1;
				break;
			case '?':
				fprintf(stderr, "Usage: x10serial [-p SERIAL_PORT] [X10COMMAND...]\n");
				break;
		}
	}

	if (debug_flag == 1) {
		printf("x10serial:Portname is %s\n",portname);
	}

	if (argc == 1) {
		// If there was only one argument then nothing was specified
		printf("x10serial: You must specify at least one X10COMMAND\n");
		printf("Try `x10serial --help' or `x10serial -h' for more information..\n");
	} else {

		// All of the command line arguments have been handled we should only have
		// the X10COMMANDS remaining.

		// optind should point to the index in argv of the next argument

		if (debug_flag == 1 ) fprintf(stdout, "x10serial:optind = %d , argc = %d\n", optind, argc);

		if (debug_flag == 1 && optind < argc) {
			// print out the remaining arguments
			fprintf(stdout,"x10serial:X10Commands found: ");
			for ( i = optind; i<argc; i++) {
				fprintf(stdout,"%s ",argv[i]);
			}
			fprintf(stdout,"\n");
		}

		// check for lock file
		// Use O_EXCL and O_CREATE to force a failure if it exists

		int lkfd;
		if (debug_flag == 1 ) fprintf(stdout, "x10serial:trying to create /var/lock/LCK..ttyACM0\n");
		while ( (lkfd = (open ("/var/lock/LCK..ttyACM0", O_RDWR | O_CREAT | O_EXCL, 0666))) == -1)
		{
			// This should be blocked
			//
			if (debug_flag == 1 ) fprintf(stdout, "x10serial:retry\n");
			sleep(1);
		}


		// open the port
		if (debug_flag == 1 ) fprintf(stdout, "x10serial:opening %s\n",portname);
		int fd = open (portname, O_RDWR | O_NOCTTY | O_SYNC);
		if (fd < 0) {
			fprintf (stdout,"error %d opening %s: %s \n", errno, portname, strerror (errno));
			remove ("/var/lock/LCK..ttyACM0");
			close (lkfd);
			return;
		}

		// Lock the file descriptor or see if locked
		if (debug_flag == 1 ) fprintf(stdout, "x10serial:locking fd\n");
		int lock = flock( fd, LOCK_EX | LOCK_NB );

		if (debug_flag == 1 ) fprintf(stdout, "x10serial:set fd attrs\n");
		set_interface_attribs (fd, B9600, 0);  // set speed to 9600 bps, 8n1 (no parity)
		//	set_blocking (fd, 1);                // set no blocking

		// Attempt to flush the port
		if (debug_flag == 1 ) fprintf(stdout, "x10serial:flush port\n");
		tcflush(fd, TCIFLUSH);

		char buf [100];
		char outbuf[100];
		int j;
		int rtn = 0;



		int n = read (fd, buf, sizeof buf);  // read up to 100 characters if ready to read
		buf [n]=0; // null terminate the string

		if (debug_flag == 1) {
			fprintf (stdout,"x10serial:Received message: %s",buf);
			fprintf (stdout,"x10serial:Consisting of %d characters.\n",n);
		}

		// Check if the Arduino has started



		if (strstr( buf, "Started") != 0) {
			if (debug_flag == 1) fprintf(stdout,"x10serial:Received message: %s\n",buf);
			// The Arduino has started and is ready for commands
			// Send any commands that we have
			if ( optind < argc) {
				// loop through all the commands
				for ( i = optind ; i < argc ; i++ ) {
					if (strlen(argv[i]) <= 100) {
						j = strlen( argv[i] );
						strncpy( outbuf , argv[i] , j );
						strncpy( outbuf+j , "\n" , 1);
						write (fd, outbuf , j+1);
						n = read (fd, buf, sizeof buf);
						buf [n] = 0;
						if ( strncmp ( buf, "OK", 2) == 0 ) {
							;
						} else if ( strncmp (buf, "ERR", 3) == 0){
							rtn=76;
						}
						if ( debug_flag == 1 ) {
							fprintf ( stdout, "x10serial:Sent %s, Received %s", argv[i], buf);
						}
					}
				}
			}
		} else {

			fprintf(stdout,"x10serial:Error!\n");
			printf("x10serial:Strncmp(%s) result %d\n.",buf,strncmp( buf, "Started" , 7));
		}
		close (fd);
		remove ("/var/lock/LCK..ttyACM0");
		close (lkfd);
	}
	return 0;
}
