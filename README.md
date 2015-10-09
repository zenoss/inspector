# Zenoss Inspector
To inspect a host, simply run the following on that host:

```bash
$ wget -q -O - https://raw.githubusercontent.com/zenoss/inspector/master/bootstrap.sh | sudo sh
```

Inspection results will be printed to stdout, and complete logs will be compressed and stored in
a dated file that looks like ```inspected-2015-10-09T12-48-47.054684.tar.gz```. If inspector detects
any problems during your inspection, it will inform you at runtime.

```
Collecting...
dfinode.sh      ✓
df.sh           ✓

diskspace.py:
The following filesystems are >= 90% full:
Filesystem     Type             Size  Used Avail Use% Mounted on
/dev/sda1      ext4              30G   12G   17G  97% /

Collecting...
etchosts.sh     ✓

Compressing results: inspected-2015-10-09T12-48-47.054684.tar.gz
Cleaning up...
```

### Adding a collector script.
If you're a dev and you find that you frequently need some set of data from installations you're
debugging, just clone the inspector repo, add a script to the ```collect``` folder, and push.
The next time someone runs the inspection, it'll run your script and save its stdout/err.

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

You add the following to that file...

```bash
#!/bin/bash

serviced service list
```

Then:

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

#### Tags
You may add a tag to your inspection script so that it is white- or black-listed appropriately
when a user runs inspect with a tag option. To do so, simply add a comment to your script
with the "zenoss-inspector-tags" prefix, followed by space-separated tags. e.g.,

```
# zenoss-inspector-tags tag1 tag2 tag3
```

### Adding a processing script.
Inspector can provide users with feedback when something looks like it might be wrong with their
system. In the example at the top of this readme, the user is being informed that one of their
filesystems is dangerously full.

To add to this capability, just drop a script into the ```process``` folder of the inspector repo.

For example, here's the script that checks the amount of inode usage:

```python
#!/usr/bin/env python

# zenoss-inspector-deps dfinode.sh

CUTOFF = 90

def main():
    with open("dfinode.sh.stdout", 'r') as f:
        lines = f.readlines()
    full = []
    for line in lines[1:]:
        try:
            pct = int(line.split()[5].replace('%', ''))
        except ValueError:
            continue
        if pct >= CUTOFF:
            full.append(line)
    if len(full) > 0:
        print "The following filesystems are using >= %d%% of their inodes:" % CUTOFF
        print lines[0].strip()
        for line in full:
            print line.strip()

if __name__ == "__main__":
    main()
```

Note the ```zenoss-inspector-deps``` tag. This defines which collector script must be executed
before your process script will run. This ensures that the data is available when your processor
script is executed.

The CWD of your script at runtime is a directory with all of the output of collector scripts that
have been executed. In the example above, ```dfinode.sh.stdout``` is used. If anything was written
to stderr by the collector script, it will be in the associated ```.stderr``` file, otherwise that
file will not exist.

Anything printed to stdout by your processor script will be immediately displayed to the user, in
red.

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
