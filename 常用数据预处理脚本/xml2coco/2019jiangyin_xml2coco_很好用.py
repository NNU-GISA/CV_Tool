# https://github.com/JialianW/pascal2coco/blob/e136f0b8d50b78e8715d2ada89397ea9b7729ef4/pascal2coco.py

import json
import xml.etree.ElementTree as ET
import os

###### 需要配置以下2项：
root_path = '/mfs/home/caoliwei/train_crop/'

my_classes = ['background','coarse']    #clw note：第二项，添加自己的class，比如person,dog,car等等；目前不知多分类是否可以


annotation_path = os.path.join(root_path, 'Annotations_val/') #clw note：所有xml保存文件路径
save_json_path = os.path.join(root_path, 'val.json') #clw note:保存json的文件路径

def load_load_image_labels(LABEL_PATH, class_name=[]):
    # temp=[]
    images=[]
    type="instances"
    annotations=[]
    #assign your categories which contain the classname and calss id
    #the order must be same as the class_nmae
    categories = [
		{
			"id" : 1,
			"name" : my_classes[1],  # 根据实际情况添加,如果像人头计数一样只有一个类别head,那么只有id=1,如果多类别就增加id=2.....
			"supercategory" : "none"
		},
	]
    # load ground-truth from xml annotations
    id_number=0
    for image_id, label_file_name in enumerate(os.listdir(LABEL_PATH)):
        print(str(image_id)+' '+label_file_name)
        label_file=LABEL_PATH + label_file_name
        image_file = label_file_name.split('.')[0] + '.jpg'
        tree = ET.parse(label_file)
        root = tree.getroot()

        size=root.find('size')
        width = float(size.find('width').text)
        height = float(size.find('height').text)
        images.append({
            "file_name": image_file,
			"height": height,
			"width": width,
			"id": image_id
		})# id of the image. referenced in the annotation "image_id"

        for anno_id, obj in enumerate(root.iter('object')):
            name = obj.find('name').text
            bbox=obj.find('bndbox')
            cls_id = class_name.index(name)  #会把my_classes传过来，这里index就是1，background的index是0
            xmin = float(bbox.find('xmin').text)
            ymin = float(bbox.find('ymin').text)
            xmax = float(bbox.find('xmax').text)
            ymax = float(bbox.find('ymax').text)
            xlen = xmax-xmin
            ylen = ymax-ymin

            assert xlen > 0, 'xlen即bbox宽度不能小于0,该图片名字为:%s, 对应的xmin, ymin为%d, %d' %(image_file, xmin, ymin)
            assert ylen > 0, 'ylen即bbox高度不能小于0,该图片名字为:%s,对应的xmin, ymin为%d, %d'  %(image_file, xmin, ymin)

            annotations.append({
                                #"segmentation" : [[xmin, ymin, xmin, ymax, xmax, ymax, xmax, ymin],],
                                "segmentation": [],
                                "area" : xlen * ylen,
                                "iscrowd": 0,
                                "image_id": image_id,
                                "bbox" : [xmin, ymin, xmax-xmin, ymax-ymin],  # clw note:根据实际情况修改
                                "category_id": cls_id,
                                "id": id_number,   #初始值id_number为0，每处理完一个xml文件，id_number+1
                                "ignore":0
                                })
            # print([image_file,image_id, cls_id, xmin, ymin, xlen, ylen])
            id_number += 1

    return {"images":images,"annotations":annotations,"categories":categories}

if __name__=='__main__':
    LABEL_PATH =  annotation_path
    classes    =  my_classes

    label_dict = load_load_image_labels(LABEL_PATH,classes)

    # with open(jsonfile,'w') as json_file:
    #     json_file.write(json.dumps(label_dict, ensure_ascii=False))
    #     json_file.close()
    with open(save_json_path, 'w', encoding='utf-8') as f:
        json.dump(label_dict, f, indent=1, separators=(',', ': '))
