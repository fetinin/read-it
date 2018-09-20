import os
import shutil

import apistar
import jinja2
from apistar import App, codecs

from app import routes


def make_doc(directory):
    app = App(routes=routes)
    codec = codecs.OpenAPICodec()
    content = codec.encode(app.document)
    document = codec.decode(content)

    loader = jinja2.PrefixLoader(
        {"apistar": jinja2.PackageLoader("apistar", "templates")}
    )
    env = jinja2.Environment(autoescape=True, loader=loader)

    template = env.get_template("apistar/docs/index.html")
    code_style = None  # pygments_css('emacs')
    output_text = template.render(
        document=document,
        langs=["javascript", "python"],
        code_style=code_style,
        static_url=lambda x: x,
    )

    output_path = os.path.join(directory, "index.html")
    if not os.path.exists(directory):
        os.makedirs(directory)
    output_file = open(output_path, "w")
    output_file.write(output_text)
    output_file.close()

    static_dir = os.path.join(os.path.dirname(apistar.__file__), "static")
    apistar_static_dir = os.path.join(directory, "apistar")
    if os.path.exists(apistar_static_dir):
        shutil.rmtree(apistar_static_dir)
    shutil.copytree(static_dir, apistar_static_dir)

    print(f"Documentation built at {output_path}")


if __name__ == "__main__":
    make_doc(directory="../docs")
