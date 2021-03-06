import re
from cmd import Cmd
import dns.resolver
import socket
import smtplib
import sys

# print(f.renderText('veriPy'))

class MyPrompt(Cmd):
    prompt = "~EmailVerifier> "
    intro = "\n\nWelcome!\n\nEnter the email you want to verify."

    def default(self, inp):
        if re.match(
            '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', inp):
            match = re.match(
                    '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', inp)
            oldDomain = re.search("@[\w.]+", inp).group()
            newDomain = oldDomain.replace("@", "")

            if match == None:
            	print('Bad Syntax')
            	raise ValueError('Bad Syntax')

            records = dns.resolver.query(newDomain, 'MX')
            for record in records:
                print(record)
            mxRecord = records[0].exchange
            print(mxRecord)
            mxRecord = str(mxRecord)

            # Get local server hostname
            host = socket.gethostname()

            # SMTP lib setup (use debug level for full output)
            server = smtplib.SMTP()
            server.set_debuglevel(0)

            # SMTP Conversation
            server.connect(mxRecord)
            server.helo(host)
            server.mail('me@domain.com')
            code, message = server.rcpt(str(inp))
            server.quit()

            # Assume 250 as Success
            if code == 250 and newDomain == 'yahoo.com' or code == 250 and newDomain == 'hotmail.com':
        	    print('Code:'+str(code)+'\n\nSuccess, but still might bounce.\n\n')
            elif code == 250:
        	    print('Code:'+str(code)+'\n\nSuccess!\n\n')
            else:
                print('Code:'+str(code)+'\n\nWill bounce.\n\n')



    def do_exit(self, input):
        print('Goodbye...')
        return True
    def help_exit(self):
        print("\n\nThis command will exit the program.\n\nTo use the 'exit' comman run:\n\nexit")
    
    # def help_verify(self):
    #     print("\n\nThis command will return if the inputted email is valid and SHOULD not bounce.\n\nTo use the 'verify' command run:\n\nverify example@email.com\n\n")

    # def do_verify(self, inp):
    #     match = re.match(
    #         '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', inp)
    #     oldDomain = re.search("@[\w.]+", inp).group()
    #     newDomain = oldDomain.replace("@", "")

    #     if match == None:
    #     	print('Bad Syntax')
    #     	raise ValueError('Bad Syntax')

    #     records = dns.resolver.query(newDomain, 'MX')
    #     print(records, "records")
    #     mxRecord = records[0].exchange
    #     mxRecord = str(mxRecord)

    #     # Get local server hostname
    #     host = socket.gethostname()

    #     # SMTP lib setup (use debug level for full output)
    #     server = smtplib.SMTP()
    #     server.set_debuglevel(0)

    #     # SMTP Conversation
    #     server.connect(mxRecord)
    #     server.helo(host)
    #     server.mail('me@domain.com')
    #     code, message = server.rcpt(str(inp))
    #     server.quit()

    #     # Assume 250 as Success
    #     if code == 250 and newDomain == 'yahoo.com':
    #     	print('Success!')
    #     elif code == 250:
    #     	print('Success, but still might bounce.')
    #     else:
    #         print('Will bounce.')

if __name__ == '__main__':
    MyPrompt().cmdloop()
