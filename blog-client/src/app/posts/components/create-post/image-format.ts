import Quill from 'quill';

interface EmbedBlot {
  new(...args: any[]): EmbedBlot;
  domNode: any;
  format(name, value);
}

const BaseImageFormat: EmbedBlot = Quill.import('formats/image');
const imageFormatAttrs = [
  'alt',
  'height',
  'width',
  'style'
];

/* Extends base image format to record more than the default styling */
export class ImageFormat extends BaseImageFormat {
  static formats(domNode) {
    return imageFormatAttrs.reduce((formats, attribute): any => {
      if (domNode.hasAttribute(attribute)) {
        formats[attribute] = domNode.getAttribute(attribute);
      }
      return formats;
    }, {});
  }

  format(name, value) {
    if (imageFormatAttrs.indexOf(name) > -1) {
      if (value) {
        this.domNode.setAttribute(name, value);
      }
      else {
        this.domNode.removeAttribute(name);
      }
    }
    else {
      super.format(name, value);
    }
  }
}
