import glob
import xml.etree.ElementTree as ET
import os


suffix = '.jpg'  # '.jpeg' 
data_dir = os.path.join(os.path.dirname(os.path.abspath('.')), 'data')
classes = ['rdq']


def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x *= dw
    w *= dw
    y *= dh
    h *= dh

    return x, y, w, h


def convert_annotation(in_file, out_file):
    """
    params: 
        in_file: annotation xml file
        out_file: file record label detail info    
    """
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text),
             float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(
            str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


def run(dataset):
    data_path = os.path.join(data_dir, dataset)
    anno_path = os.path.join(data_dir, dataset + '_annotations')
    train_file = os.path.join(data_dir, 'train.txt')
    train_fh = open(train_file, 'w')
    # if test file is needed
    # test_file = os.path.join(data_dir, 'test.txt')
    # test_fh = open(test_file, 'w')
    image_paths = glob.glob(os.path.join(data_path, '*'))
    for image_path in image_paths:
        basename = image_path.split('/')[-1].split(suffix)[0]
        anno_file = os.path.join(anno_path, basename+'.xml')
        out_fh = open(os.path.join(data_path, basename + '.txt'), 'w')
        if os.path.exists(anno_file):
            in_fh = open(anno_file)
            convert_annotation(in_fh, out_fh)
            # only train image with label
            # train_fh.write(image_path+'\n')
            # test_fh.write(image_path+'\n')
        # train image without annotation file
        train_fh.write(image_path+'\n')
        # test_fh.write(image_path+'\n')
        out_fh.close()
        in_fh.close()

    train_fh.close()


if __name__ == '__main__':
    for dataset in ['rdq']:
        run(dataset)

