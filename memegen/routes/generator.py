from flask import Blueprint, current_app as app, render_template
from flask_api.decorators import set_renderers
from flask_api.renderers import HTMLRenderer

from ._common import url_for


blueprint = Blueprint('generator', __name__, url_prefix="/generator")


# TODO: Deduplicate with `overview#_gen`
def _gen():
    for template in sorted(app.template_service.all()):
        path = template.sample_path
        url = url_for("image.get", key=template.key, path=path, _external=True)
        link = url_for("links.get", key=template.key, path=path)
        yield {
            'name': template.name,
            'url': url,
            'link': link
        }


@blueprint.route("")
@set_renderers(HTMLRenderer)
def get():
    imgs = [img for img in _gen()]
    # TODO: In the future, this could be provided via query param (similar to top/bottom)
    selected_img = imgs[0]
    selected_img['selected'] = True
    return render_template('generator.html', imgs=imgs, selected_img=selected_img)
