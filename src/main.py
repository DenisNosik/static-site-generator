import os
import shutil


def generate_destination(destination):
    if os.path.exists(destination):
        shutil.rmtree(destination) # delete destination dir
        print(destination, "deleted")
    os.mkdir(destination)
    print(destination, "created")

def copy_all_content_to(source, destination):
    if not os.path.exists(source):
        raise Exception("source doesn't exist")
    for item in os.listdir(source):
        path = os.path.join(source, item)
        print("work with:", item, "and path is", path)
        if os.path.isfile(path):
            print(path, "is a file. Copy to", destination)
            shutil.copy(path, destination)
        else:
            destination_path = os.path.join(destination, item)
            print(item, "is dir. destination path is", destination_path)
            if not os.path.exists(destination_path):
                print(destination_path, "doesn't exist. Creating.")
                os.mkdir(destination_path)
            print("Recursion...")
            copy_all_content_to(path, destination_path)

def main():
    generate_destination("public")
    copy_all_content_to("static", "public")

if __name__ == "__main__":
    main()
