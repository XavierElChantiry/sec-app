import exifread
import PIL
from PIL import Image

#things added just to do the risk assesment part
import base64
import re
import os
from datetime import datetime


imager_to_iterate = [
    "Images/Activation.png", 
    "Images/Brain-Channel.png", 
    "Images/Brain.png",
    "Images/Chemicals.png",
    "Images/Dopamine.png",
    "Images/Music.png",]
# metadata_results = {}
secret_message = []



def check_timestamp_anomalies(file_path, exif_date_str):
    try:
        fs_created_ts = os.path.getctime(file_path)
        fs_modified_ts = os.path.getmtime(file_path)
        fs_created = datetime.fromtimestamp(fs_created_ts)
        fs_modified = datetime.fromtimestamp(fs_modified_ts)

        exif_date_str = str(exif_date_str).strip()[:19]
        exif_date = datetime.strptime(exif_date_str, '%Y:%m:%d %H:%M:%S')

        if exif_date > fs_created:
            # exif date after creation date
            return True

        time_diff = fs_modified - exif_date
        # file modified
        if time_diff.days > 0:
             return True
        return False
    except Exception as e:
        return False


def extract_metadata(image_path):
    risk_score  = 0
    risk_list = []

    target_fields = {
            "GPS Latitude": "GPS GPSLatitude",
            "GPS Longitude": "GPS GPSLongitude",
            "Date Original": "EXIF DateTimeOriginal",
            "Create Date": "Image DateTime",
            "Modify Date": "EXIF DateTimeDigitized",
            "Camera Make": "Image Make",
            "Camera Model": "Image Model",
            "Software": "Image Software",
            "User Comment": "EXIF UserComment",
            "Description": "Image ImageDescription",
            "maker note" : "EXIF MakerNote", 
            "copyright" :  "Image Copyright",
        }
    
    with open(image_path, "rb") as file_handle:
        tags = exifread.process_file(file_handle)
        # print("\n exifread data only\n",tags)
        # print(tags)
        for label, tag in target_fields.items():
            val = tags.get(tag, "Not Found")
            # metadata_results[label] = val
            if val != "Not Found":
                if label in ["User Comment", "Description", "maker note"]:
                    risk_list.append("Hidden Secret")
                    secret_message.append(val)
                    risk_score +=10
                elif label == "copyright": #this is makeshift
                    risk_list.append("Hidden Secret")
                    # secret_message.append(val)
                    risk_score +=10
                elif label == "GPS Latitude":
                    risk_list.append("Privacy leak")
                    risk_score +=5
                elif label == "Software":
                    risk_list.append("Editing(these are png so no jpeg compression)")
                    risk_score +=5
                if label == "Date Original":
                    if(check_timestamp_anomalies(image_path, val)):
                        risk_list.append("timestamp anomaly")
                        risk_score +=5
                print(f"|{label:<15}| {val}")

    try:
        img = Image.open(image_path)
        info = img.info
        
        for lognval in info:
            if lognval in ["Software", "xmp", 'Make', 'Model', 'create-date', 'Copyright']:
                # decode if it ends with =
                val_str = str(info[lognval])
                xml_match = re.search(r'<exif:MakerNote>(.*?)</exif:MakerNote>', val_str)
                try:
                    decoded = base64.b64decode(info[lognval], validate=True).decode('utf-8')
                    # print(decoded)
                    
                    print(f"|{lognval:<15}| {decoded}")
                    risk_score += 5
                    risk_list.append("Encoded secret message")
                    secret_message.append(decoded)

                except:
                    if xml_match:
                        # print(xml_match.group(1))
                        
                        print(f"|{lognval:<15}| {xml_match.group(1)}")
                        risk_score += 10
                        risk_list.append("XML secret message")
                        secret_message.append(xml_match.group(1))
                    elif lognval == "Software" and "Editing(these are png so no jpeg compression)" not in risk_list:

                        print(f"|{lognval:<15}| {info[lognval]}")
                        risk_score += 10
                        risk_list.append("Hidden Secret 'Software' used for secret message")
                        secret_message.append(info[lognval])


                    # else:
                    #     print(lognval , info[lognval])
    

    except Exception as e:
        print(f"Error processing {image_path}: {e}")

    print("\n------------ summary ---------------")
    print("risk score = ",risk_score)
    print("risk cause of risk score ",risk_list)
    print("------------------------------------")



def main():
    for image_path in imager_to_iterate:
        print("\n■■■■ Metadata Extraction for", image_path, "■■■■")
        extract_metadata(image_path)
    print("\n---------secret messages------------" )
    for i in dict.fromkeys(secret_message):
        print(i)

if __name__ == "__main__":
    main()