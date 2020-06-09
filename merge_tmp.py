import moviepy.editor as mpe
import os


# Function to compose video and audio
def composeVA(videoName, audioName):
    video = mpe.VideoFileClip(videoName)
    background_music = mpe.AudioFileClip(audioName)
    final_clip = video.set_audio(background_music)
    return final_clip


download_path_tmp = "C:\\Users\\hgmnj\\Desktop\\Youtube_Download\\tmp\\"
download_path_final = "C:\\Users\\hgmnj\\Desktop\\Youtube_Download\\final\\"

list = os.listdir(download_path_tmp)
names = ["", ""]
elem = ["", ""]
for j in range(0, len(list)):
    if "mp4" in list[j]:
        names[0] = list[j].split("_Video")[0]
        elem[0] = list[j]
    else:
        names[1] = list[j].split("_Audio")[0]
        elem[1] = list[j]
    print(names)
    if names[0] in names[1] and names[0] != '':
        video_output = composeVA(download_path_tmp + elem[0], download_path_tmp + elem[1])
        video_output.write_videofile(download_path_final + names[0] + ".mp4")

        # cleaning the tmp folder
        os.remove(download_path_tmp + elem[0])
        os.remove(download_path_tmp + elem[1])
        print("tmp cleaned")
    else:
        print("Nope")

list = os.listdir(download_path_tmp)
print("Files remaining in the tmp folder: ", list)

