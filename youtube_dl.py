# imports
import pytube
import moviepy.editor as mpe
import os
import tqdm


# Function to compose video and audio
def composeVA(videoName, audioName):
    video = mpe.VideoFileClip(videoName)
    background_music = mpe.AudioFileClip(audioName)
    final_clip = video.set_audio(background_music)
    return final_clip


# inputs
download_path_tmp = "C:\\Users\\hgmnj\\Desktop\\Youtube_Download\\tmp\\"
download_path_final = "C:\\Users\\hgmnj\\Desktop\\Youtube_Download\\final\\"
advancement_file_path = "C:\\Users\\hgmnj\\Desktop\\Youtube_Download\\adv.txt"
# playlist_bool_test = input("Youtube playlist (y/n):")
# url = input("Input the url here: ")
# mp = input("Download format (mp4/mp3): ")


url = "https://www.youtube.com/watch?v=-fuddRv5ME4"
mp = "mp4"
playlist_bool_test = "n"


# test playlist bool validity
def testIFplaylist(playlist):
    if playlist == "y":
        playlist_bool = True
    elif playlist == "n":
        playlist_bool = False
    else:
        playlist_bool = None
    return playlist_bool


while testIFplaylist(playlist_bool_test) is None:
    playlist_bool_test = input("<Playlist type error> Please input either y or n:")


# Download of the video
def getBESTquality(quality, listStreams):
    for j in range(len(listStreams)):
        if quality in str(listStreams[j]):
            return quality, j
    return None, 0


# Function to check download progress
def progress_Check(stream=None, chunk=None, file_handle=None, remaining=None):
    # Gets the percentage of the file that has been downloaded.
    percent = (100 * (file_size - remaining)) / file_size
    # print("{:00.0f}% downloaded".format(percent))
    progress_bar.refresh()
    progress_bar.n = file_size - remaining


# Change Tilte Name (switch spaces with underscores)
def switchSpaceUnderscore(title):
    newTitle = ""
    for i in title:
        if i == " ":
            newTitle += "_"
        elif i == "/":
            newTitle += "_"
        else:
            newTitle += i
    return newTitle


qualityList = ["1080", "720", "480", "360", "240", "144"]
global file_size
global progress_bar


if playlist_bool_test == "n":
    a = True
    while a:
        try:
            yt = pytube.YouTube(url, on_progress_callback=progress_Check)
            a = False
        except:
            print("Connection Error")
            a = True
    title = switchSpaceUnderscore(yt.title)
    # video download
    already_dl = 0
    resultsList = yt.streams.filter(adaptive=True, subtype=mp).all()
    k = 0
    qualityResult, index = getBESTquality(qualityList[k], resultsList)
    while qualityResult is None:
        k = k+1
        qualityResult, index = getBESTquality(qualityList[k], resultsList)
    print("The video will be downloaded with a quality of:", qualityResult)
    file_size = resultsList[index].filesize
    progress_bar = tqdm.tqdm(total=file_size)
    progress_bar.set_description("Video")
    resultsList[index].download(output_path=download_path_tmp, filename=title+'_Video')
    progress_bar.close()

    # audio download
    resultsList = yt.streams.filter(adaptive=True, only_audio=True, subtype="webm").all()
    file_size = resultsList[0].filesize
    progress_bar = tqdm.tqdm(total=file_size)
    progress_bar.set_description("Audio")
    resultsList[0].download(output_path=download_path_tmp, filename=title+'_Audio')
    progress_bar.close()

    # creating the final video
    video_output = composeVA(download_path_tmp+title+'_Video.'+mp, download_path_tmp+title+'_Audio.webm')
    video_output.write_videofile(download_path_final+yt.title+".mp4")

    # cleaning the tmp folder
    os.remove(download_path_tmp+title+'_Video.'+mp)
    os.remove(download_path_tmp+title+'_Audio.webm')
    print("tmp cleaned")
else:
    try:
        pl = pytube.Playlist(url)
    except:
        print("Connection Error")

    length_playlist = len(pl.parse_links())
    playlist = pl.parse_links()
    v = 1  # Last downloaded video in the playlist
    print("Nbr of videos in the playlist: ", length_playlist)
    while v != length_playlist:
        connected = False
        print("Video ", v+1, " of ", length_playlist)
        for tryhard in range(50):
            try:
                yt = pytube.YouTube(playlist[v], on_progress_callback=progress_Check)
                connected = True
            except:
                print(tryhard, ": Connection Error")
            if connected:
                break
        title = switchSpaceUnderscore(yt.title)
        # video download
        resultsList = yt.streams.filter(adaptive=True, subtype=mp).all()
        k = 0
        qualityResult, index = getBESTquality(qualityList[k], resultsList)
        while qualityResult is None:
            k = k + 1
            qualityResult, index = getBESTquality(qualityList[k], resultsList)
        print("The video will be downloaded with a quality of:", qualityResult)
        file_size = resultsList[index].filesize
        progress_bar = tqdm.tqdm(total=file_size)
        progress_bar.set_description("Video")
        resultsList[index].download(output_path=download_path_tmp, filename=title + '_Video')
        progress_bar.close()

        # audio download
        resultsList = yt.streams.filter(adaptive=True, only_audio=True, subtype="webm").all()
        file_size = resultsList[0].filesize
        progress_bar = tqdm.tqdm(total=file_size)
        progress_bar.set_description("Audio")
        resultsList[0].download(output_path=download_path_tmp, filename=title + '_Audio')
        progress_bar.close()

        # # creating the final video
        # # print(os.listdir(download_path_tmp))
        # video_output = composeVA(download_path_tmp + title + '_Video.' + mp, download_path_tmp + title + '_Audio.webm')
        # video_output.write_videofile(download_path_final + title + ".mp4")
        #
        # # cleaning the tmp folder
        # os.remove(download_path_tmp + title + '_Video.' + mp)
        # os.remove(download_path_tmp + title + '_Audio.webm')
        # print("tmp cleaned")
        v = v + 1
