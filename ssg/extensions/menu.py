from cProfile import label
from ssg import hooks, parsers


def collect_files(source, site_parsers):
    valid = lambda p : not p.isinstance(parsers.parsers.ResourceParser)
    files = []

    for path in source.rglob("*"):
        for parser in list(filter(valid, site_parsers)):
            if parser.valid_file_ext(path.suffix):
                files.append(path)
    
    return files

hooks.register('collect_files', collect_files)

def generate_menu(html, ext):
    template = '<li><a href="{}{}">{}</a></li>'
    menu_item = lambda name, ext : template.format((name, ext, name))
    return template

hooks.register('generate_menu', generate_menu)
