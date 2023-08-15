from PIL import Image

def convert_jpg_to_rgba_png(input_file, output_file):
    try:
        # Open the JPG image
        image = Image.open(input_file)

        # Convert to RGBA
        rgba_image = image.convert("RGBA")

        # Save as PNG
        rgba_image.save(output_file, "PNG")

        print("JPG to RGBA PNG conversion successful.")
    except IOError:
        print("Cannot convert JPG to RGBA PNG.")
        
# Example usage:
input_file = "EmeraldLake.jpeg"  # Replace with the path to your JPG image
output_file = "EmeraldLake.png"  # Replace with the desired output file path

convert_jpg_to_rgba_png(input_file, output_file)