# Zenoss Inspector

## Limitations
* Currently only works on Centos/RHEL
* Some steps may fail for Zenoss Core

## Making Contributions
Pull requests welcome.

Zenoss staff interested in making changes should refer to this [document describing the code change process ](https://docs.google.com/document/d/14TvBCIjC3Hb_WWqMs5naLAlPcpWcE70cUWFAE_5o8hY) for inspector.

## Inspecting a host

### Quick & dirty inspection
To inspect a host, simply run the following on that host:

```bash
$ curl -s https://raw.githubusercontent.com/zenoss/inspector/master/bootstrap.sh | sudo sh
```

Inspection results will be printed to stdout, and complete logs will be compressed and stored in
a dated file that looks like ```inspected-2015-10-09T12-48-47.054684.tar.gz```. If inspector detects
any problems during your inspection, it will inform you at runtime.

```
free.sh                      done
dfinode.sh                   done
df.sh                        done
ps-aux.sh                    done
diskspace.py                 done
The following filesystems are >= 90% full:
Filesystem     Type             Size  Used Avail Use% Mounted on
/dev/sda1      ext4              30G   29G    1G  97% /
docker-version.sh            done
etchosts.sh                  done
docker-container-logs.py     done
netstat-plant.sh             done
docker-images.sh             done
uname-a.sh                   done
localhost-loopback.py        done
inodes.py                    done
docker-running.sh            done
Compressing results: inspected-2015-10-09T12-48-47.054684.tar.gz
Cleaning up...
```

### Inspecting with options
Inspections can be performed with a handful of options. To use inspector in this fashion, just
download the master branch, unzip it, and run inspect:

```
$ wget -q https://github.com/zenoss/inspector/archive/master.zip
$ unzip -q master.zip
$ cd inspector-master
$ ./inspect -h

usage: inspect [-h] [--no-remove] [--no-save] [-j JOBS] [-t TIMEOUT]
               [-w WHITELIST [WHITELIST ...] | -b BLACKLIST [BLACKLIST ...]]

Inspect a Zenoss installation.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         Print version and exit.
  --print-tags          Print tags and exit.
  --no-remove           Don't remove working directory.
  --no-save             Don't compress results.
  -j JOBS, --jobs JOBS  Maximum number of jobs to run in parallel.
  -t TIMEOUT, --timeout TIMEOUT
                        Timeout in seconds for entire inspection.
  -l LINES, --lines LINES
                        Limit output of each result file to LINES lines. Set
                        to 0 to collect all lines. Default is 100000.
  -w WHITELIST [WHITELIST ...], --whitelist WHITELIST [WHITELIST ...]
                        Use only these tags.
  -b BLACKLIST [BLACKLIST ...], --blacklist BLACKLIST [BLACKLIST ...]
                        Don't use these tags.
```

## Adding scripts
There's two kinds of scripts inspector uses to collect and process host information - collector
and info scripts. Collector scripts are executed and their stdout and stderr are stored in a
newly created directory. Examples include collecting disk space usage, memory usage, and system log
files. Info scripts are a little different - their output is printed to stdout in a scary red color.
The purpose of info scripts is to inform the user that something may need investigating. Examples
include checking for full disks, excessive memory usage, or errors in logs.

### Script directives
Directives can be added to inspector scripts to indicate how they should be used. Add a directive to a script
by simply adding a comment with the directive in it. See examples below.

#### zenoss-inspector-tags
Add a comment to your script with ```zenoss-inspector-tags``` followed by a space-separated list of
tags that should be applied to your script at runtime.

##### Example
```bash
#!/bin/bash

# zenoss-inspector-tags slow filesystem

lsof
```

Users can whitelist or blacklist tags at runtime. For example, if a user wanted to run only scripts
tagged ```filesystem```, they would use the following command:

```bash
$ ./inspect -w filesystem
```

Alternatively, they could blacklist slow scripts thus:

```bash
$ ./inspect -b slow
```

#### zenoss-inspector-deps
Add a comment to your script with ```zenoss-inspector-deps``` followed by a space-separated list of
dependencies. Your script will not be executed until/unless its dependencies have been met.

##### Example
Suppose there are already two inspector scripts, ```a.sh``` & ```b.sh```, upon which your third
script, ```c.sh```, should depend. Here's what ```c.sh``` might look like:

```bash
#!/bin/bash

# zenoss-inspector-deps a.sh b.sh

diff a.sh.stdout b.sh.stdout
```

#### zenoss-inspector-info
Add a comment to your script with ```zenoss-inspector-info```. This will redirect the stdout of your
script to the tty of the user running inspect, in red to indicate an there might be a problem. This
should only be used to indicate a possible issue, not for general output.

##### Example
```bash
#!/bin/bash

# zenoss-inspector-info

echo "There's a problem!"
```

### A complete example: warn the user if Docker isn't running.

We'll need two scripts for this example: a collector script and an info script. Let's start with
the collector.

Under ```inspector/scripts```, make a new script and name it ```ps-aux.sh```. Place the following
into it:

```bash
#!/bin/bash

# zenoss-inspector-tags process

ps aux
```

Now let's run inspector like this:

```bash
$ ./inspect --no-save --no-remove -w process
ps-aux.sh     done
```

Here we're instructing inspector to not create a tarball (```--no-save```), not remove the
working directory (```--no-remove```) and to whitelist scripts tagged ```process```, which is what we
tagged our script with. Inspector indicates that our script was run. We should now have a new
directory that looks something like ```inspected-2015-10-11T11-18-11.347149```, and inside we should
see at least two files: ```ps-aux.sh.stdout``` and ```inspector.log```.

Now that we've collected a list of processes running on the system, let's write a script that will
warn the user if the Docker daemon is not on that list.

Create a new script under ```inspector/scripts``` and name it ```docker-running.sh```. Place the
following inside it:

```bash
#!/bin/bash

# zenoss-inspector-info
# zenoss-inspector-tags process docker
# zenoss-inspector-deps ps-aux.sh

grep "docker -d" ps-aux.sh.stdout &>/dev/null

if [ $? -ne 0 ]
    then
        grep "docker daemon" ps-aux.sh.stdout &>/dev/null
        if [ $? -ne 0 ]
            then echo "Docker doesn't appear to be running."
        fi
fi
```

Take a look at the ```zenoss-inspector-*``` directives we've added. ```zenoss-inspector-info``` instructs
inspector to direct the stdout of this script immediately to the user.
```zenoss-inspector-tags process docker``` tags our new script ```process``` and ```docker```.
```zenoss-inspector-deps ps-aux.sh``` instructs inspector to wait for the ```ps-aux.sh``` script
to finish executing successfully before kicking off our new script.

Note that this script is looking in ```ps-aux.sh.stdout``` in the current working directory. Collector
script output filenames are appended with ```.stdout``` or ```.stderr```, and all scripts are executed
within the directory that contains those output files.

Now let's run inspector again:
```
./inspect --no-save --no-remove -w process
ps-aux.sh             done
docker-running.sh     done
```

Looks good. If I stop docker and run it again:

```
$ sudo stop docker
docker stop/waiting

$ ./inspect --no-save --no-remove -w process
ps-aux.sh             done
docker-running.sh     done
Docker doesn't appear to be running.
```

Once you commit your new scripts and push them to github, they will be executed the next time
someone kicks off an inspection.
