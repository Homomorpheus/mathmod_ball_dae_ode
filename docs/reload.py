from livereload import Server, shell
import subprocess

def copy():
    subprocess.run("cp -r ../src .".split())
    subprocess.run("jupyter book build .".split())

server = Server()
server.watch('./*', shell('jupyter book build .', cwd='.'))
server.watch("../src/*", copy)
server.serve(root='./_build/html', open_url_delay=3)
