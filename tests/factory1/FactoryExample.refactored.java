
public interface ProductsAbstract{
	public DecodedImage getDecodeImage();
}

class DecodedImage {
    private String image;

    public DecodedImage(String image) {
        this.image = image;
    }

    public String toString() {
        return image + ": is decoded";
    }
}


class GifReader implements ProductsAbstract {
    private DecodedImage decodedImage;

    public GifReader(String image, int size) {
        this.decodedImage = new DecodedImage(image);
    }

    public DecodedImage getDecodeImage() {
        return decodedImage;
    }
}

class JpegReader implements ProductsAbstract {
    private DecodedImage decodedImage;

    public JpegReader(String image, int size) {
        decodedImage = new DecodedImage(image);
    }

    public DecodedImage getDecodeImage() {
        return decodedImage;
    }
}

public class FactoryMethod {
	ProductsAbstract createGifReader(String image, int size){
		return new GifReader(image,size);
	}
	ProductsAbstract createJpegReader(String image, int size){
		return new JpegReader(image,size);
	}

    ProductsAbstract reader =createJpegReader (image,size)
    public static void main(String[] args) {
        DecodedImage decodedImage = new DecodedImage();
        String image = args[0];
        String format = image.substring(image.indexOf('.') + 1, (image.length()));
        if (format.equals("gif")) {
            ProductsAbstract reader =createGifReader (image,size);
        }
        if (format.equals("jpeg")) {
            ProductsAbstract reader =createJpegReader (image,size);
        }
        assert reader != null;
        decodedImage = reader.getDecodeImage();
        System.out.println(decodedImage);
    }
}
