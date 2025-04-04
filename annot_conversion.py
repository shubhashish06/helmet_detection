import os
import xml.etree.ElementTree as ET

def convert_to_yolo_format(xml_file, output_dir):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Extract image dimensions
    size = root.find('size')
    width = int(size.find('width').text)
    height = int(size.find('height').text)

    # Prepare YOLO formatted annotations
    yolo_annotations = []

    for obj in root.findall('object'):
        class_name = obj.find('name').text
        if class_name == 'head':
            class_id = 0
        elif class_name == 'helmet':
            class_id = 1
        else:
            continue  # Skip unknown classes

        bndbox = obj.find('bndbox')
        xmin = int(bndbox.find('xmin').text)
        ymin = int(bndbox.find('ymin').text)
        xmax = int(bndbox.find('xmax').text)
        ymax = int(bndbox.find('ymax').text)

        # Convert to YOLO format
        x_center = (xmin + xmax) / 2.0 / width
        y_center = (ymin + ymax) / 2.0 / height
        box_width = (xmax - xmin) / width
        box_height = (ymax - ymin) / height

        yolo_annotations.append(f"{class_id} {x_center} {y_center} {box_width} {box_height}")

    # Write to output file
    output_file = os.path.join(output_dir, os.path.basename(xml_file).replace('.xml', '.txt'))
    with open(output_file, 'w') as f:
        f.write("\n".join(yolo_annotations))

def process_directory(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith('.xml'):
            xml_file = os.path.join(input_dir, filename)
            convert_to_yolo_format(xml_file, output_dir)

# Example usage
input_directory = '/Users/ashish/Desktop/final_projects/helmet_detection/dataset/annotations'
output_directory = '/Users/ashish/Desktop/final_projects/helmet_detection/dataset/annotations_txt'
process_directory(input_directory, output_directory)
