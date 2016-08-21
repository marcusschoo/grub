import subprocess
import tempfile
import os

class TextInterface:
    def __init__(self):
        self.file = tempfile.NamedTemporaryFile(mode='w+b',delete=False)
        self.file_path = self.file.name
        print 'Interfacing through temporary file:', self.file.name

    def append(self, line):
        self.file.write('%s\n' % line)

    def run(self):
        self.file.close()
        subprocess.call(["open","-e","-W",self.file_path])

    def get_line(self):
        self.file = open(self.file_path)
        for line in self.file:
            yield line.strip()

    def __del__(self):
        self.reset()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.reset()

    def reset(self):
        os.remove(self.file_path)

# Example Usage

ti = TextInterface()
ti.append('one')
ti.append('two')
ti.run()
for line in ti.get_line():
    print '>', line
