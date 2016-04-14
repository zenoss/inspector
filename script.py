
import os
from threading import Thread
from subprocess import Popen, PIPE

ZI_TAGS = "zenoss-inspector-tags"
ZI_DEPS = "zenoss-inspector-deps"
ZI_INFO = "zenoss-inspector-info"
ZI_FILE = "zenoss-inspector-files" # script writes output files directly to the target dir

class Script(object):

    def __init__(self, script):
        self.script = script
        self.basename = os.path.basename(script)
        self.tags = []
        self.load_tags()
        self.deps = []
        self.load_dependencies()
        self.info = self.get_info_tag()
        self.files = self.get_files_tag()

    def load_tags(self):
        with open(self.script, 'r') as f:
            lines = f.readlines()
        for line in lines:
            if ZI_TAGS in line:
                self.tags = line[line.index(ZI_TAGS) + len(ZI_TAGS):].strip().split()
                return

    def load_dependencies(self):
        with open(self.script, 'r') as f:
            lines = f.readlines()
        for line in lines:
            if ZI_DEPS in line:
                self.deps = line[line.index(ZI_DEPS) + len(ZI_DEPS):].strip().split()
                return

    def get_info_tag(self):
        with open(self.script, 'r') as f:
            raw = ''.join(f.readlines())
        if ZI_INFO in raw:
            return True
        return False

    def get_files_tag(self):
        with open(self.script, 'r') as f:
            raw = ''.join(f.readlines())
        if ZI_FILE in raw:
            return True
        return False

    def __run(self, cwd, queue):
        if self.info:
            p = Popen(self.script, stdout=PIPE, stderr=PIPE, cwd=cwd)
            stdout, stderr = p.communicate()
            queue.put({
                "script": self,
                "stdout": stdout,
                "stderr": stderr,
                "retcode": p.returncode
            })
        else:
            if self.files:
                outDir = os.path.join(cwd, os.path.splitext(self.basename)[0])
                os.mkdir(outDir)
                cmd = [self.script, os.path.abspath(outDir)]
            else:
                cmd = self.script

            fout = open(os.path.join(cwd, self.basename + ".stdout"), 'w')
            ferr = open(os.path.join(cwd, self.basename + ".stderr"), 'w')
            p = Popen(cmd, stdout=fout, stderr=ferr, cwd=cwd)
            p.communicate()
            queue.put({
                "script": self,
                "retcode": p.returncode
            })

    def run(self, cwd, queue):
        t = Thread(target=self.__run, args=(cwd, queue))
        t.setDaemon(True)
        t.start()
