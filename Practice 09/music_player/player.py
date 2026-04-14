import pygame
import os
class MusicPlayer:
    def __init__(self, music_folder):
        pygame.mixer.init()
        self.playlist = self.load_playlist(music_folder)
        self.current_index = 0
        self.state = "STOPPED"
        self.start_time = 0
    def load_playlist(self, folder):
        files = []
        for file in os.listdir(folder):
            if file.endswith(".wav") or file.endswith(".mp3"):
                files.append(os.path.join(folder, file))
        files.sort()
        return files
    def play(self):
        if not self.playlist:
            return
        track = self.playlist[self.current_index]
        pygame.mixer.music.load(track)
        pygame.mixer.music.play()
        self.state = "PLAYING"
        self.start_time = pygame.time.get_ticks()
    def stop(self):
        pygame.mixer.music.stop()
        self.state = "STOPPED"
    def next(self):
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.play()
    def previous(self):
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.play()
    def get_current_track_name(self):
        if not self.playlist:
            return "No tracks"
        return os.path.basename(self.playlist[self.current_index])
    def get_progress(self):
        if self.state != "PLAYING":
            return 0
        elapsed_ms = pygame.time.get_ticks() - self.start_time
        return elapsed_ms // 1000