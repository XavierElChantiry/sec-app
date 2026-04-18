from PIL import Image
import stepic




def extract_hidden(file_name):
    log_filename = "architect_manifesto.txt"
    with open(log_filename, "w") as log_file:
        image = Image.open(file_name)
        data = stepic.decode(image) 
        log_file.write(data)
        # print(data)
        return data




if __name__ == "__main__":
    print(extract_hidden("evidence.png"))
