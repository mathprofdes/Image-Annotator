Annotations
===========

The program allows the user to add several simple annotations to the image.  Each of the annotation objects have their own attributes.  If the user requires more annotation options they can use this program for some of the easier annotations and then copy the image into a more sophisticated image editor to finish their work.

The order that the annotations are drawn is not determined by the order that they are input (as with most graphical editors), the order is determined by the type of annotation that is being input.  The graphical order from top to bottom is,

- Text Boxes
- Rectangles
- Ellipses
- Lines
- Arrows
- Images

Text Boxes
^^^^^^^^^^

A text box annotation is just plain (unformatted) text that is included in the image.  This annotation allows the user to insert just the text or include a rectangular box around the text.

.. figure:: Images/Snapshot3.png
    :alt: Text Box

    Text Box

Text Box Options
""""""""""""""""

- **Show**: This is a check box that allows the user to toggle the showing of the annotation.  You can also double-click the annotation item in the annotation lest to toggle the showing of the annotation.
- **Text**: This is the text that is displayed.  It is simply plain text but can be multiline.
- **Text Color**: This is the color of the displayed text.  The displayed text is unformatted so you cannot have different colors for different characters in the text.
- **Font**: This is the font that is being used for the text.  You may select any font that is currently on your system for this option.
- **Font Size**: This is the pixel size of the displayed text.  Although this can be set along with font we included it in the set of options since it requires less steps to change and will probably be used more often than changing the font.
- **Anchor X Position**: This is the horizontal pixel position of the anchor point for the text box, which is the upper left corner of the text box.
- **Anchor Y Position**: This is the vertical pixel position of the anchor point for the text box, which is the upper left corner of the text box.
- **Justify**: This is the text justification within the text box.
- **Include Box**: This is a check box that allows the user to include a box around the annotation.  The other options in that section adjust the appearance of the box if it is included.
- **Background Color**: This is the color of the background for the box.
- **Border Color**: This is the color of the box border.
- **Border Width**: This is the pixel width of the border.
- **Horizontal Padding**: This is the additional horizontal padding used for the text box.  This is included with the box option on or off but really is noticeable only when the box is selected.
- **Vertical Padding**: This is the additional vertical padding used for the text box.  This is included with the box option on or off but really is noticeable only when the box is selected.
- **Rotation**: This is the amount of rotation that is applied to the text box.
- **Transparency**:  This is the amount of transparency that is applied to the text box.


Rectangles
^^^^^^^^^^

A rectangle annotation is simply an open or closed rectangle that can have rounded corners. These are good for pointing out interesting aspects of a graph or for putting a fancier border around some text or mathematical expression.  If you do use it for a text or expression border note that these objects are not linked to text or expression boxes so they need to positioned independently.

.. figure:: Images/Snapshot5.png
    :alt: Rectangle Annotation

    Rectangle Annotation


Rectangle Options
"""""""""""""""""

- **Show**: This is a check box that allows the user to toggle the showing of the annotation.  You can also double-click the annotation item in the annotation lest to toggle the showing of the annotation.
- **Color**: This is the color of the border of the rectangle.
- **Line Width**: This is the pixel width of the border of the rectangle.
- **Anchor X Position**: This is the horizontal pixel position of the anchor point for the rectangle, which is the upper left corner of the rectangle.
- **Anchor Y Position**: This is the vertical pixel position of the anchor point for the rectangle, which is the upper left corner of the rectangle.
- **Width**: This is the pixel width of the rectangle.
- **Height**: This is the pixel height of the rectangle.
- **Fill Rectangle**: This is a check box that controls if the inside of the rectangle is filled or transparent.
- **Fill Color**: If the fill option is selected this is the color of the inside area.
- **Corner Radius**: This is the radius of the curve used for the corners of the rectangle.  The rectangle is really a rounded rectangle.  If the corner radius is 0 then the rectangle has sharp corners and the larger this value the more circular the corners of the rectangle become.

Ellipses
^^^^^^^^

An ellipse annotation is simply an open or closed ellipse. These are good for pointing out interesting aspects of a graph or for putting a fancier border around some text or mathematical expression.  If you do use it for a text or expression border note that these objects are not linked to text or expression boxes so they need to positioned independently.

.. figure:: Images/Snapshot6.png
    :alt: Ellipse Annotation

    Ellipse Annotation


Ellipse Options
"""""""""""""""

- **Show**: This is a check box that allows the user to toggle the showing of the annotation.  You can also double-click the annotation item in the annotation lest to toggle the showing of the annotation.
- **Color**: This is the color of the border of the ellipse.
- **Line Width**: This is the pixel width of the border of the ellipse.
- **Anchor X Position**: This is the horizontal pixel position of the anchor point for the ellipse, which is the upper left corner of the box containing the ellipse.
- **Anchor Y Position**: This is the vertical pixel position of the anchor point for the ellipse, which is the upper left corner of the box containing the ellipse.
- **Width**: This is the pixel width of the ellipse.
- **Height**: This is the pixel height of the ellipse.
- **Fill Ellipse**: This is a check box that controls if the inside of the ellipse is filled or transparent.
- **Fill Color**: If the fill option is selected this is the color of the inside area.

Lines
^^^^^

An line annotation is simply a line segment from one position on the graph to another. These are good for pointing to places on the graph, especially combined with text or expression annotations.  If you do use it with a text or expression note that these objects are not linked to text or expression boxes so they need to positioned independently.

.. figure:: Images/Snapshot7.png
    :alt: Line Annotation

    Line Annotation

Line Options
""""""""""""

- **Show**: This is a check box that allows the user to toggle the showing of the annotation.  You can also double-click the annotation item in the annotation lest to toggle the showing of the annotation.
- **Color**: This is the color of the line.
- **Line Width**: This is the pixel width of the line.
- **Start X Position**: This is the horizontal pixel position of the starting point for the line.
- **Start Y Position**: This is the vertical pixel position of the starting point for the line.
- **End X Position**: This is the horizontal pixel position of the ending point for the line.
- **End Y Position**: This is the vertical pixel position of the ending point for the line.

Arrows
^^^^^^

An arrow annotation is simply a line segment from one position on the graph to another with the addition of an arrowhead at the ending position. These are good for pointing to places on the graph, especially combined with text or expression annotations.  If you do use it with a text or expression note that these objects are not linked to text or expression boxes so they need to positioned independently.

.. figure:: Images/Snapshot8.png
    :alt: Arrow Annotation

    Arrow Annotation

Arrow Options
"""""""""""""

- **Show**: This is a check box that allows the user to toggle the showing of the annotation.  You can also double-click the annotation item in the annotation lest to toggle the showing of the annotation.
- **Color**: This is the color of the arrow.
- **Line Width**: This is the pixel width of the arrow.
- **Start X Position**: This is the horizontal pixel position of the starting point for the arrow.
- **Start Y Position**: This is the vertical pixel position of the starting point for the arrow.
- **End X Position**: This is the horizontal pixel position of the ending point for the arrow.
- **End Y Position**: This is the vertical pixel position of the ending point for the arrow.
- **Arrow Size**: This is a pixel size of the size of the arrowhead.
- **Arrow Angle**: This is the angle used at the point for the angular width of the arrowhead.


Images
^^^^^^

An image annotation is an image that is rendered inside the graph. This option is useful for including better mathematical renderings using an outside equation editor to create a mathematical expression as an image.  It can also be used to insert logos and images that cn be superimposed over the graph.  This option allows the user to make the image semitransparent so that the graph can be seen through the image.

.. figure:: Images/Snapshot9.png
    :alt: Image Annotation

    Image Annotation

Image Options
"""""""""""""

- **Show**: This is a check box that allows the user to toggle the showing of the annotation.  You can also double-click the annotation item in the annotation lest to toggle the showing of the annotation.
- **Image**: This is the image that is displayed.  There is a small toolbar above the image that allows the user to past an image from the clipboard or load an image from an image file.  Note that large images can consume computer resources and be slow to process.  Keep these images reasonable in size, if you wish to load in a large image it may be better to scale the image down with image editing software before loading the image into the annotator.
- **Anchor X Position**: This is the horizontal pixel position of the anchor point for the text box, which is the upper left corner of the text box.
- **Anchor Y Position**: This is the vertical pixel position of the anchor point for the text box, which is the upper left corner of the text box.
- **Scaling**: This sets the scaling factor of the image.
- **Aspect Ratio**: This sets the aspect ratio of the image.
- **Flip Horizontally**: This reflects the image horizontally.
- **Flip Vertically**: This reflects the image vertically.
- **Rotation**: This is the amount of rotation that is applied to the image.
- **Use Transparent Color**: This enables a transparent color, every pixel in the image that matches the transparent color is set to transparent.
- **Transparent Color**: This is the color to use as the transparent color if the option is enabled. Every pixel in the image that matches the transparent color is set to transparent.
- **Image Transparency**:  This is the amount of transparency that is applied to the entire image.
- **Include Box**: This is a check box that allows the user to include a box around the annotation.  The other options in that section adjust the appearance of the box if it is included.
- **Padding Color**: This is the color of the background for the box.
- **Border Color**: This is the color of the box border.
- **Border Width**: This is the pixel width of the border.
- **Horizontal Padding**: This is the additional horizontal padding used for the box.
- **Vertical Padding**: This is the additional vertical padding used for the box.
