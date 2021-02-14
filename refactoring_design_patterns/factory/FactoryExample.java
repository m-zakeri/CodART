
class DecodedImage {
    private String image;

    public DecodedImage(String image) {
        this.image = image;
    }

    public String toString() {
        return image + ": is decoded";
    }
}


class GifReader {
    private DecodedImage decodedImage;

    public GifReader(String image, int size) {
        this.decodedImage = new DecodedImage(image);
    }

    public DecodedImage getDecodeImage() {
        return decodedImage;
    }
}

class JpegReader {
    private DecodedImage decodedImage;

    public JpegReader(String image, int size) {
        decodedImage = new DecodedImage(image);
    }

    public DecodedImage getDecodeImage() {
        return decodedImage;
    }
}

public class FactoryMethod {
    JpegReader reader = new JpegReader(image);
    public static void main(String[] args) {
        DecodedImage decodedImage = new DecodedImage();
        String image = args[0];
        String format = image.substring(image.indexOf('.') + 1, (image.length()));
        if (format.equals("gif")) {
            GifReader reader = new GifReader(image);
        }
        if (format.equals("jpeg")) {
            JpegReader reader = new JpegReader(image);
        }
        assert reader != null;
        decodedImage = reader.getDecodeImage();
        System.out.println(decodedImage);
    }
}
