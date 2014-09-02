inspector
=========

Inspector collects data from a host and posts it to the inspector server for easy sharing.

To run the inspector, log into the machine you'd like to inspect and run:

```
wget -q -O - zenpip.zendev.org:1774/bootstrap | sh
```

You may be asked for your password in order to run as root. (You'll need to be part of the sudoers group on the target machine.)

Inspector will present you with a link to view the data collection results.

It's easy to get inspector to gather more data, too. Clone the repo, add a script you'd like the output of to inspector/inspector/scripts, and mark it as executable. Commit your change and push it to the repo. The inspector server will be updated with your changes and the next time someone runs inspector, it'll collect the data you wanted.
