from ..domain import Image

from ._base import Service


class ImageService(Service):

    def __init__(self, template_store, image_store, debug=False, **kwargs):
        super().__init__(**kwargs)
        self.template_store = template_store
        self.image_store = image_store
        self.debug = debug

    def find_template(self, key):
        template = self.template_store.read(key)
        if not template:
            raise self.exceptions.TemplateNotFound
        return template

    def create_image(self, template, text):
        image = Image(template, text)
        if not self.image_store.exists(image) or self.debug:
            try:
                self.image_store.create(image)
            except OSError as exception:
                if "name too long" in str(exception):
                    raise self.exceptions.FilenameTooLong from None
                else:
                    raise exception from None
        return image
