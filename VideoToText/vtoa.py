import subprocess

def VtoA(file,outputd,**kwargs):
    if "ffmpeg" in kwargs:
        ffmpeg = kwargs["ffmpeg"]
    else:
        ffmpeg = 'ffmpeg'
    out = f'{ffmpeg} -i "{file}" "{outputd}"'
    print(out)
    subprocess.run(out)