import pickle
from PIL import Image, ImageOps
import random

#print("reading...")
# Open the file in read-binary mode ('rb')
#with open("files/IAM-32.pickle", "rb") as f:
#    data = pickle.load(f)

#print(data["train"].keys())  # Prints the loaded object
#print(data['train']['670'])  # Prints the loaded object


def file_reader(file_path, len_transcr, img_height): 
    print("reading...")
    gtfile = file_path + "/ascii/lines.txt"
    info = []
    for line in open(gtfile):
        if not line.startswith("#"):
            line_segment = line.strip().split()
            image_id = line_segment[0].split("-")[1]
            name = line_segment[0]
            writer_name = int(name.split("-")[0])
            img_path = file_path + "/lines/" + str(writer_name) + "/" + str(name)
            #t = line_segment[8:].split("|")
            t = line_segment[8:][0].split("|")
            if len(t) > 1:
                continue
            #transcr = ' '.join(line_segment[8:])
            transcr = t[0]
            #print(transcr)
            if len(transcr) > 20:
                continue
            else:
                info.append([img_path, transcr, writer_name, image_id])

    random.shuffle(info)

    split_idx = int(len(info) * 0.8)
    # Split into train and validation sets
    info_train = info[:split_idx]
    info_val = info[split_idx:]

    print("len train set: ", len(info_train))
    print("len val set: ", len(info_val))

    dataset_train = {}
    dataset_val = {}
    for i, (img_path, transcr, writer_name, img_id) in enumerate(info_train):
        if len(transcr) > len_transcr: # CHANGED, doesn't accept too long transcriptions(?)
            continue
        if i % 1000 == 0:
            print('imgs: [{}/{} ({:.0f}%)]'.format(i, len(info_train), 100. * i / len(info_train)))
        img = Image.open(img_path + '.png').convert('RGB') #.convert('L')

        # Convert image into new height/width
        new_height = img_height
        aspect_ratio = img.width / img.height
        new_width = int(new_height * aspect_ratio)
        #print("new width: ", new_width)
        if new_width > 10:
            img = img.resize((new_width, new_height))
        else:
            print("too small width")
            continue


        if str(writer_name) in dataset_train:
            dataset_train[str(writer_name)].append({"img": img, "label": transcr, "img_id": img_id})
        else:
            dataset_train[str(writer_name)] = [{"img": img, "label": transcr, "img_id": img_id}]
    
    for i, (img_path, transcr, writer_name, img_id) in enumerate(info_val):
        if len(transcr) > len_transcr: # CHANGED, doesn't accept too long transcriptions(?)
            continue
        if i % 1000 == 0:
            print('imgs: [{}/{} ({:.0f}%)]'.format(i, len(info_val), 100. * i / len(info_val)))
        img = Image.open(img_path + '.png').convert('RGB') #.convert('L')

        # Convert image into new height/width
        new_height = img_height
        aspect_ratio = img.width / img.height
        new_width = int(new_height * aspect_ratio)
        img = img.resize((new_width, new_height))


        if str(writer_name) in dataset_val:
            dataset_val[str(writer_name)].append({"img": img, "label": transcr, "img_id": img_id})
        else:
            dataset_val[str(writer_name)] = [{"img": img, "label": transcr, "img_id": img_id}]

    return dataset_train, dataset_val

#dataset_dict = file_reader("files/riksarkivet_data")
                
