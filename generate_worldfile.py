import argparse
import os
import requests
from PIL import Image
from io import BytesIO

def get_geology_map(x1, y1, x2, y2, width=3840, height=2160):
    base_url = "https://map.bgs.ac.uk/arcgis/services/BGS_Detailed_Geology/MapServer/WMSServer"
    layers = "BGS.50k.Bedrock"
    styles = "default"
    format_type = "image/gif"
    crs = "EPSG:27700"

    bbox = f"{x1},{y1},{x2},{y2}"

    params = {
        "REQUEST": "GetMap",
        "VERSION": "1.3.0",
        "LAYERS": layers,
        "STYLES": styles,
        "FORMAT": format_type,
        "CRS": crs,
        "BBOX": bbox,
        "WIDTH": width,
        "HEIGHT": height
    }

    response = requests.get(base_url, params=params)
    image = Image.open(BytesIO(response.content))

    return image

def calculate_world_file_parameters(x1, y1, x2, y2, width, height):
    pixel_size_x = (x2 - x1) / width
    pixel_size_y = (y2 - y1) / height

    a = pixel_size_x
    b = 0.0
    c = 0.0
    d = -pixel_size_y

    e = x1
    f = y2

    return a, b, c, d, e, f

def main():
    parser = argparse.ArgumentParser(description="Get geology map image based on bounding box coordinates.")
    parser.add_argument("x1", type=float, help="X-coordinate of the first point")
    parser.add_argument("y1", type=float, help="Y-coordinate of the first point")
    parser.add_argument("x2", type=float, help="X-coordinate of the second point")
    parser.add_argument("y2", type=float, help="Y-coordinate of the second point")
    parser.add_argument("-o", "--output", type=str, default=".", help="Output folder destination")

    args = parser.parse_args()

    map_image = get_geology_map(args.x1, args.y1, args.x2, args.y2)


    jpeg_image = map_image.convert("RGB")

    output_folder = args.output
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, "BGS_Bedrock_1_50k.jpg")
    jpeg_image.save(output_path)

    a, b, c, d, e, f = calculate_world_file_parameters(args.x1, args.y1, args.x2, args.y2, width=3840, height=2160)
    world_file_path = os.path.join(output_folder, "BGS_Bedrock_1_50k.jgw")
    with open(world_file_path, "w") as world_file:
        world_file.write(f"{a}\n{b}\n{c}\n{d}\n{e}\n{f}\n")

    png_file_path = os.path.join(output_folder, "BGS_Bedrock_1_50k.png")
    if os.path.exists(png_file_path):
        os.remove(png_file_path)

    print(f"Geology map saved to: {output_path}")
    print(f"World file saved to: {world_file_path}")

if __name__ == "__main__":
    main()
