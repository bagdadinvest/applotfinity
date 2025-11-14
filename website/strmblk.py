from wagtail.blocks import RichTextBlock, StructBlock, StreamBlock
from wagtail.images.blocks import ImageChooserBlock

class AppStreamBlock(StreamBlock):
    heading = RichTextBlock(
        features=["h2", "h3", "bold", "italic"], 
        icon="title", 
        label="Heading"
    )
    paragraph = RichTextBlock(icon="pilcrow", label="Paragraph")
    image = ImageChooserBlock(icon="image", label="Image")

    class Meta:
        icon = "placeholder"
        label = "App Content Blocks"
