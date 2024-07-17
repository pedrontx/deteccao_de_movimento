from pytube import YouTube

# URL do vídeo do YouTube
video_url = 'https://www.youtube.com/watch?v=dxsawQOQ9lU&ab_channel=CoolVision'

# Criar objeto YouTube
yt = YouTube(video_url)

# Selecionar o stream de vídeo com a maior resolução disponível
stream = yt.streams.get_highest_resolution()

# Baixar o vídeo
stream.download(output_path='.', filename='video_baixado_teste_2.mp4')

print("Download concluído!")
