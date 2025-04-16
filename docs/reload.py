from livereload import Server, shell
server = Server()
server.watch('./*', shell('jupyter book build .', cwd='.'))
server.serve(root='./_build/html', open_url_delay=3)
