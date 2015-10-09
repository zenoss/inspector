# Zenoss Inspector

To inspect a host, simply run the following:

```bash
$ wget -q -O - https://raw.githubusercontent.com/zenoss/inspector/master/bootstrap.sh | sudo sh
```

```
Collecting...
dfinode.sh      ✓
df.sh           ✓
etchosts.sh     ✓

Compressing results: inspected-2015-10-09T12-48-47.054684.tar.gz
Cleaning up...
```

Inspection results will be printed to stdout, and complete logs will be compressed and stored in
a dated file that looks like ```inspected-2015-10-09T12-36-59.574053.tar.gz```.

### man inspect

```
usage: inspect [-h] [--no-remove] [-w WHITELIST [WHITELIST ...] | -b BLACKLIST
               [BLACKLIST ...]]

Inspect a Zenoss installation.

optional arguments:
  -h, --help            show this help message and exit
  --no-remove           Don't remove untarred directory.
  -w WHITELIST [WHITELIST ...], --whitelist WHITELIST [WHITELIST ...]
                        Use only these tags.
  -b BLACKLIST [BLACKLIST ...], --blacklist BLACKLIST [BLACKLIST ...]
                        Don't use these tags.
```

### Adding a collector script.

If you're a dev and you find that you frequently need some set of data from installations you're
debugging, just clone out the inspector repo, add a script to it, and push. The next time someone
runs the inspection, it'll include your script and its output.

By way of example:

```bash
$ git clone git@github.com:zenoss/inspector.git
Cloning into 'inspector'...
remote: Counting objects: 116, done.
remote: Compressing objects: 100% (14/14), done.
remote: Total 116 (delta 4), reused 0 (delta 0), pack-reused 97
Receiving objects: 100% (116/116), 204.13 KiB | 0 bytes/s, done.
Resolving deltas: 100% (34/34), done.
Checking connectivity... done.

$ cd inspector/

$ tree
.
├── bootstrap.sh
├── collect
│   ├── dfinode.sh
│   ├── df.sh
│   └── etchosts.sh
├── inspect
├── makefile
├── process
│   ├── diskspace.py
│   └── inodes.py
├── README.md
└── termcolor.py

2 directories, 10 files

$ vim collect/serviced-service-list.sh
```

(You add the following to that file.)

```bash
#!/bin/bash

serviced service list
```

```bash
$ chmod +x collect/serviced-service-list.sh

$ git add collect/serviced-service-list.sh

$ git commit ...

$ git push ...
```

Then, the next time somebody runs the inspector via the onliner above:

```bash
$ wget -q -O - https://raw.githubusercontent.com/zenoss/inspector/master/bootstrap.sh | sudo sh

$ ./inspect

Collecting...
etchosts.sh                  ✓
dfinode.sh                   ✓
serviced-service-list.sh     ✓
df.sh                        ✓

Compressing results: inspected-2015-10-09T12-52-50.311993.tar.gz
Cleaning up...

```
