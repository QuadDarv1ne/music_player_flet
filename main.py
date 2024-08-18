import flet as ft
import os
import shutil
from tinytag import TinyTag
from math import pi
import asyncio

class MusicPlayer:
    def __init__(self, page):
        self.page = page
        self.index = 0
        self.state = ""
        self.audio_controls = []
        self.tracks_list = [
            "sounds/outfoxing.mp3",
            "sounds/param_viper.mp3",
            "sounds/track_drums.mp3",
        ]
        self.volume = 0.5
        self.sounds_folder = 'sounds'
        if not os.path.exists(self.sounds_folder):
            os.makedirs(self.sounds_folder)

        # Определение стилей
        self.styles = {
            "default": {
                "bgcolor": ft.colors.BLUE_700,
                "text_color": ft.colors.BLUE_500,
                "button_color": ft.colors.BLUE_400,
                "volume_icon": ft.icons.VOLUME_UP,
                "volume_slider": ft.colors.BLUE_400
            },
            "dark": {
                "bgcolor": ft.colors.GREY_700,
                "text_color": ft.colors.GREY_500,
                "button_color": ft.colors.GREY_400,
                "volume_icon": ft.icons.VOLUME_UP,
                "volume_slider": ft.colors.GREY_400
            },
            "light": {
                "bgcolor": ft.colors.GREEN_700,
                "text_color": ft.colors.GREEN_500,
                "button_color": ft.colors.GREEN_400,
                "volume_icon": ft.icons.VOLUME_UP,
                "volume_slider": ft.colors.GREEN_400
            },
            "sunset_dreams": {
                "bgcolor": ft.colors.AMBER_500,
                "text_color": ft.colors.AMBER_500,
                "button_color": ft.colors.ORANGE_300,
                "volume_icon": ft.icons.VOLUME_UP,
                "volume_slider": ft.colors.ORANGE_300
            },
            "ocean_breeze": {
                "bgcolor": ft.colors.LIGHT_BLUE_500,
                "text_color": ft.colors.LIGHT_BLUE_500,
                "button_color": ft.colors.TEAL_400,
                "volume_icon": ft.icons.VOLUME_UP,
                "volume_slider": ft.colors.TEAL_400
            },
            "midnight_blue": {
                "bgcolor": ft.colors.BLACK,
                "text_color": ft.colors.BLACK,
                "button_color": ft.colors.BLUE_300,
                "volume_icon": ft.icons.VOLUME_UP,
                "volume_slider": ft.colors.BLUE_300
            },
            "forest_green": {
                "bgcolor": ft.colors.GREEN_500,
                "text_color": ft.colors.GREEN_500,
                "button_color": ft.colors.LIGHT_GREEN_300,
                "volume_icon": ft.icons.VOLUME_UP,
                "volume_slider": ft.colors.LIGHT_GREEN_300
            },
            "retro_vibes": {
                "bgcolor": ft.colors.BROWN_900,
                "text_color": ft.colors.ORANGE_200,
                "button_color": ft.colors.BROWN_700,
                "volume_icon": ft.icons.VOLUME_UP,
                "volume_slider": ft.colors.ORANGE_200
            },
            "neon_lights": {
                "bgcolor": ft.colors.BLACK,
                "text_color": ft.colors.CYAN_ACCENT_700,
                "button_color": ft.colors.GREEN_ACCENT_400,
                "volume_icon": ft.icons.VOLUME_UP,
                "volume_slider": ft.colors.CYAN_ACCENT_700
            },
            "pastel_harmony": {
                "bgcolor": ft.colors.WHITE,
                "text_color": ft.colors.PINK_400,
                "button_color": ft.colors.LIGHT_GREEN_300,
                "volume_icon": ft.icons.VOLUME_UP,
                "volume_slider": ft.colors.LIGHT_GREEN_300
            },
            "mountain_hike": {
                "bgcolor": ft.colors.GREY_900,
                "text_color": ft.colors.BROWN_400,
                "button_color": ft.colors.BROWN_600,
                "volume_icon": ft.icons.VOLUME_UP,
                "volume_slider": ft.colors.BROWN_600
            },
            "vibrant_citrus": {
                "bgcolor": ft.colors.YELLOW_500,
                "text_color": ft.colors.BLACK,
                "button_color": ft.colors.ORANGE_400,
                "volume_icon": ft.icons.VOLUME_UP,
                "volume_slider": ft.colors.ORANGE_400
            }
        }
        self.current_style = "default"

    def change_style(self, e):
        styles_list = list(self.styles.keys())
        current_index = styles_list.index(self.current_style)
        self.current_style = styles_list[(current_index + 1) % len(styles_list)]
        self.update_style()
        self.page.update()

    def update_style(self):
        style = self.styles[self.current_style]
        self.page.bgcolor = style["bgcolor"]  # Установка цвета фона страницы
        self.current_time.color = style["text_color"]
        self.remaining_time.color = style["text_color"]
        self.track_name.color = style["text_color"]
        self.track_artist.color = style["text_color"]
        self.progress_bar.bgcolor = style["button_color"]
        self.volume_icon.name = style["volume_icon"]
        self.volume_slider.active_color = style["volume_slider"]

    def pick_files_result(self, e: ft.FilePickerResultEvent):
        if e.files:
            for f in e.files:
                try:
                    src = f.path.replace("\\", "/")
                    filename = os.path.basename(src)
                    dest = os.path.join(self.sounds_folder, filename)
                    shutil.copy(src, dest)
                    self.tracks_list.append(dest)

                    audio1 = ft.Audio(
                        src=dest,
                        autoplay=False,
                        volume=self.volume,
                        balance=0,
                        on_position_changed=self.progress_change,
                        on_state_changed=self.check_state,
                    )
                    self.audio_controls.append(audio1)
                    self.page.overlay.append(audio1)

                    audio_info = TinyTag.get(dest)
                    self.track_name.value = audio_info.title if audio_info.title else "Неизвестное название"
                    self.track_artist.value = audio_info.artist if audio_info.artist else "Неизвестный исполнитель"

                except Exception as ex:
                    print(f"Ошибка при обработке файла {f.path}: {ex}")

            self.update_track_list()
            self.page.update()
        else:
            print("Отмена")

    def check_state(self, e):
        if e.data == "completed":
            self.next_track(None)
        self.page.update()

    def play_track(self, e):
        if not self.audio_controls:
            print("Нет доступных треков для воспроизведения")
            return

        if self.state == "":
            self.state = "playing"
            self.btn_play.icon = ft.icons.PAUSE_CIRCLE
            self.audio_controls[self.index].play()
        elif self.state == "playing":
            self.state = "paused"
            self.btn_play.icon = ft.icons.PLAY_CIRCLE
            self.audio_controls[self.index].pause()
        else:
            self.state = "playing"
            self.btn_play.icon = ft.icons.PAUSE_CIRCLE
            self.audio_controls[self.index].resume()
        self.page.update()

    def new_track(self):
        self.disc_image.rotate.angle += pi * 2
        audio = TinyTag.get(self.audio_controls[self.index].src)
        self.track_name.value = audio.title if audio.title else "Неизвестное название"
        self.track_artist.value = audio.artist if audio.artist else "Неизвестный исполнитель"
        self.current_time.value = "0:0"
        self.remaining_time.value = self.converter_time(audio.duration * 1000)
        self.progress_track.value = 0.0

        for audio_control in self.audio_controls:
            audio_control.pause()

        if self.state == "playing":
            self.audio_controls[self.index].volume = self.volume
            self.audio_controls[self.index].play()

        self.page.update()

    def next_track(self, e):
        if not self.audio_controls:
            print("Нет доступных треков для воспроизведения")
            return

        self.audio_controls[self.index].pause()
        self.index = (self.index + 1) % len(self.audio_controls)
        self.new_track()
        self.page.update()

    def previous_track(self, e):
        if not self.audio_controls:
            print("Нет доступных треков для воспроизведения")
            return

        self.audio_controls[self.index].pause()
        self.index = (self.index - 1) % len(self.audio_controls)
        self.new_track()
        self.page.update()

    def seek_forward(self, e):
        if not self.audio_controls:
            print("Нет доступных треков для воспроизведения")
            return

        current_position = self.audio_controls[self.index].position
        new_position = current_position + 10000
        if new_position > self.audio_controls[self.index].duration * 1000:
            new_position = self.audio_controls[self.index].duration * 1000
        print(f"Seeking forward: Current Position: {current_position}, New Position: {new_position}")
        self.audio_controls[self.index].position = new_position
        self.progress_change(ft.Event(data=new_position))
        self.page.update()

    def seek_backward(self, e):
        if not self.audio_controls:
            print("Нет доступных треков для воспроизведения")
            return

        current_position = self.audio_controls[self.index].position
        new_position = current_position - 10000
        if new_position < 0:
            new_position = 0
        print(f"Seeking backward: Current Position: {current_position}, New Position: {new_position}")
        self.audio_controls[self.index].position = new_position
        self.progress_change(ft.Event(data=new_position))
        self.page.update()

    def volume_change(self, e):
        if not self.audio_controls:
            print("Нет доступных треков для воспроизведения")
            return

        v = e.control.value
        self.audio_controls[self.index].volume = 0.01 * v
        self.volume = 0.01 * v
        if v == 0:
            self.volume_icon.name = ft.icons.VOLUME_OFF
        elif 0 < v <= 50:
            self.volume_icon.name = ft.icons.VOLUME_DOWN
        else:
            self.volume_icon.name = ft.icons.VOLUME_UP
        self.page.update()

    @staticmethod
    def converter_time(millis):
        millis = int(millis)
        seconds = (millis // 1000) % 60
        minutes = (millis // (1000 * 60)) % 60
        return f"{int(minutes)}:{int(seconds):02d}"

    def progress_change(self, e):
        if not self.audio_controls:
            print("Нет доступных треков для воспроизведения")
            return

        audio = TinyTag.get(self.audio_controls[self.index].src)
        self.current_time.value = self.converter_time(e.data)
        self.remaining_time.value = self.converter_time((audio.duration * 1000) - int(e.data))
        self.progress_track.value = float(e.data) / (audio.duration * 1000)
        self.page.update()

    def update_track_list(self):
        # Обновите элемент интерфейса списка треков, если у вас есть такой элемент
        pass

    def on_progress_bar_click(self, e):
        if not self.audio_controls:
            print("Нет доступных треков для воспроизведения")
            return

        print(f"Click event data: {e.data}")
        if e.data and 'x' in e.data:
            click_position = e.data['x']
            print(f"Progress bar clicked at: {click_position}")

            progress_width = self.progress_bar.width
            print(f"Progress bar width: {progress_width}")

            if 0 <= click_position <= progress_width:
                new_position = (click_position / progress_width) * (self.audio_controls[self.index].duration * 1000)
                print(f"Setting new position: {new_position}")
                self.audio_controls[self.index].position = new_position
                self.progress_change(ft.Event(data=new_position))
                self.page.update()

    def build_ui(self):
        self.pick_files_dialog = ft.FilePicker(on_result=self.pick_files_result)
        self.upload_button = ft.IconButton(
            icon=ft.icons.UPLOAD_FILE,
            icon_size=35,
            on_click=lambda _: self.pick_files_dialog.pick_files(
                allow_multiple=True,
                file_type=ft.FilePickerFileType.AUDIO
            )
        )
        self.style_button = ft.IconButton(
            icon=ft.icons.STYLE,
            icon_size=35,
            on_click=self.change_style
        )

        for track in self.tracks_list:
            audio = ft.Audio(
                src=track,
                autoplay=False,
                volume=self.volume,
                balance=0,
                on_position_changed=self.progress_change,
                on_state_changed=self.check_state,
            )
            self.audio_controls.append(audio)
            self.page.overlay.append(audio)

        audio_init = TinyTag.get(self.audio_controls[self.index].src)

        self.current_time = ft.Text(value="0:0")
        self.remaining_time = ft.Text(value=self.converter_time(audio_init.duration * 1000))
        self.progress_bar = ft.Container(
            width=400,
            height=8,
            bgcolor=self.styles[self.current_style]["button_color"],
            on_click=self.on_progress_bar_click
        )
        self.progress_track = ft.Container(
            width=400,
            height=8,
            bgcolor=ft.colors.BLUE,
        )
        self.track_name = ft.Text(value=audio_init.title if audio_init.title else "Неизвестное название")
        self.track_artist = ft.Text(value=audio_init.artist if audio_init.artist else "Неизвестный исполнитель")
        self.btn_play = ft.IconButton(icon=ft.icons.PLAY_CIRCLE, icon_size=35, on_click=self.play_track)
        self.volume_icon = ft.Icon(name=self.styles[self.current_style]["volume_icon"])

        # Установите значение слайдера громкости в соответствии с текущей громкостью
        self.volume_slider = ft.Slider(
            width=150,
            active_color=self.styles[self.current_style]["volume_slider"],
            min=0,
            max=100,
            divisions=100,
            value=self.volume * 100,
            label="{value}",
            on_change=self.volume_change,
        )

        self.disc_image = ft.Image(
            src="assets/album.png",
            width=180,
            height=180,
            fit=ft.ImageFit.CONTAIN,
            rotate=ft.transform.Rotate(0, alignment=ft.alignment.center),
            animate_rotation=ft.animation.Animation(300, ft.AnimationCurve.EASE_IN_CIRC),
        )

        main_content = ft.Card(
            content=ft.Container(
                content=ft.Row(
                    [
                        ft.Container(width=80, height=300),
                        ft.Column(
                            [
                                ft.ListTile(
                                    leading=ft.Icon(ft.icons.MUSIC_NOTE_ROUNDED),
                                    title=self.track_name,
                                    subtitle=self.track_artist,
                                ),
                                ft.Row(
                                    [self.current_time, self.progress_bar, self.remaining_time],
                                    alignment=ft.MainAxisAlignment.END,
                                ),
                                ft.Row(
                                    [
                                        ft.IconButton(
                                            icon=ft.icons.SKIP_PREVIOUS,
                                            icon_size=35,
                                            on_click=self.previous_track,
                                        ),
                                        self.btn_play,
                                        ft.IconButton(
                                            icon=ft.icons.SKIP_NEXT,
                                            icon_size=35,
                                            on_click=self.next_track,
                                        ),
                                        self.volume_icon,
                                        self.volume_slider,  # Используйте слайдер громкости
                                        self.upload_button,
                                        self.style_button,
                                    ],
                                    alignment=ft.MainAxisAlignment.END,
                                ),
                            ]
                        ),
                    ]
                ),
            ),
            right=-10,
            width=620,
            color=ft.colors.ON_PRIMARY,
            height=180,
        )

        stack = ft.Stack(
            controls=[
                main_content,
                self.disc_image,
                self.pick_files_dialog,
            ],
            width=700,
            height=300,
        )

        self.page.add(stack)

async def monitor_new_tracks(player: MusicPlayer):
    while True:
        files_in_folder = os.listdir(player.sounds_folder)
        if files_in_folder:
            for filename in files_in_folder:
                if not filename.endswith(".mp3"):
                    continue
                full_path = os.path.join(player.sounds_folder, filename)
                if full_path not in player.tracks_list:
                    player.tracks_list.append(full_path)
                    audio1 = ft.Audio(
                        src=full_path,
                        autoplay=False,
                        volume=player.volume,
                        balance=0,
                        on_position_changed=player.progress_change,
                        on_state_changed=player.check_state,
                    )
                    player.audio_controls.append(audio1)
                    player.page.overlay.append(audio1)
                    player.update_track_list()
                    player.page.update()
        await asyncio.sleep(3)

async def main(page: ft.Page):
    page.title = "Музыкальный плеер"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.height = 300
    page.window.width = 800
    page.window.min_width = 800
    page.window.min_height = 300

    player = MusicPlayer(page)
    player.build_ui()

    asyncio.create_task(monitor_new_tracks(player))

ft.app(target=main)

'''

'''