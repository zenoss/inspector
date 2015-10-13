
import os
from subprocess import Popen, PIPE, CalledProcessError, check_call

ZI_TAGS = "zenoss-inspector-tags"
ZI_DEPS = "zenoss-inspector-deps"
ZI_INFO = "zenoss-inspector-info"

class Script(object):

    def __init__(self, script):
        self.script = script
        self.basename = os.path.basename(script)
        self.tags = []
        self.load_tags()
        self.deps = []
        self.load_dependencies()
        self.info = self.get_info_tag()

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

    def run(self, cwd):
        p = Popen(self.script, stdout=PIPE, stderr=PIPE, cwd=cwd)
        stdout, stderr = p.communicate()
        return stdout, stderr, p.returncode

    def store_result(self, stdout, stderr, result_path):
        fout = os.path.join(result_path, self.basename + ".stdout")
        with open(fout, 'w') as f:
            f.write(stdout)
        if len(stderr) > 0:
            ferr = os.path.join(result_path, self.basename + ".stderr")
            with open(ferr, 'w') as f:
                f.write(stderr)
